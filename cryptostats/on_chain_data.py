"""
Get on-chain data from web3
"""

from web3 import Web3

from .config import CONFIG

class OnChainData():
	"""
	On chain data retreival class
	"""

	web3_client = None

	@classmethod
	def get_client(cls):
		"""
		Get the web3 client
		"""

		if cls.web3_client is None:
			cls.web3_client = Web3(Web3.HTTPProvider(CONFIG['infura_url']))

		return cls.web3_client

	@classmethod
	def get_block_height(cls) -> int:
		"""
		Returns the current ethereum blockchain height
		"""
		client = cls.get_client()
		return client.eth.block_number

	@classmethod
	def get_block_transaction_count(cls, block: int=None):
		"""
		Returns the number of transactions confirmed in a given block, if no block is given it
		will default to the most recent block
		"""
		block = block or cls.get_block_height()
		client = cls.get_client()
		return client.eth.get_block_transaction_count(block)

	@classmethod
	def get_gas_price(cls, units: str='gwei'):
		"""
		Gets the current network gas price
		"""
		client = cls.get_client()
		return round(float(Web3.fromWei(client.eth.gas_price, units)), 1)

	@classmethod
	def get_balance(cls, account: str, units: str='ether'):
		"""
		Gets the balance of a given account
		"""

		client = cls.get_client()
		return float(Web3.fromWei(client.eth.get_balance(account), units))