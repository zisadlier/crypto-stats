"""
Base API Wrapper
"""

from abc import ABC, abstractmethod

class BaseApiWrapper(ABC):
	"""
	Abstract API wrapper class
	"""

	@abstractmethod
	def get_base_url(self) -> str:
		"""
		Base url for requests
		"""
		return None
