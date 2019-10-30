import numpy as np

class Q_Table:

	def __init__(self, num_states, num_actions, shape, converge_val): 
		self.shape = shape
		# self.prev_q_matrix = np.zeros((num_states, num_actions))
		self.q_matrix = np.ones((num_states, num_actions))
		self.converge_val = converge_val

	def get_qVal(self, states):
		statesID = self.get_stateID(states)
		return self.q_matrix[statesID, :]

	def update_qVal(self, learning_rate, states, actions, td_error):

		temp = self.q_matrix.copy()

		statesID = self.get_stateID(states)
		currentActionsIndex = self._mapFromTrueActionsToIndex(actions)
		self.q_matrix[statesID, currentActionsIndex] += learning_rate * td_error

		if self._hasConverged(temp, self.q_matrix):
			return True
		else:
			return False


	def _hasConverged(self, q_mat1, q_mat2):
		diff = np.linalg.norm(q_mat1 - q_mat2)

		if abs(diff) < self.converge_val:
			return True

		else: 
			return False


	def get_stateID(self,states):

		assert isinstance(states, np.ndarray)

		ids = []

		num_rows, num_cols = self.shape

		Nt = self._augState(states[0])
		ht = self._augState(states[1])
		temp_id = Nt * num_cols + ht
		return temp_id

	def get_TDerror(self, states, actions, next_states, next_actions, reward, gamma, is_done):
		statesID = self.get_stateID(states)
		currentActionsIndex = self._mapFromTrueActionsToIndex(actions)
		current_qVal = self.q_matrix[statesID, currentActionsIndex]

		if is_done:
			next_qVal = 0
		else:
			next_statesID = self.get_stateID(next_states)
			nextActionsIndex = self._mapFromTrueActionsToIndex(next_actions)
			next_qVal = self.q_matrix[next_statesID, nextActionsIndex]

		return reward + (gamma*next_qVal) - current_qVal

	def save_q_state(self, file):
		np.save(file+'/q_mat', self.q_matrix)

	def _augState(self, stateVal):
		"""
		Augment state value so that [-3,3] goes to [0,6] 
		"""
		return stateVal+3

	def _mapFromTrueActionsToIndex(self, actions):
		if actions == -1:
			return 1 
		elif actions == 1:
			return 2
		else:
			return 0 



