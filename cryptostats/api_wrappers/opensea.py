"""
Wrapper classes to make calls to the OpenSea API
"""

from typing import Dict

import requests

from .base import BaseApiWrapper
from ..enums import VolumeTimeFrame

class OpenSeaWrapper(BaseApiWrapper):
	"""
	Main OpenSea API wrapper
	"""

	def get_base_url(self) -> str:
		return 'https://api.opensea.io/api/v1/'

	# Collection methods
	def get_collection_data(self, collection_id: str) -> dict:
		"""
		Gets all data associated with a given NFT collection from the API
		"""

		base_url = self.get_base_url()
		req = requests.get(f'{base_url}collection/{collection_id}')

		return req.json()['collection']

	def get_image_url(self, collection_id: str) -> str:
		"""
		Gets the url of the main image for the collection
		"""

		data = self.get_collection_data(collection_id)
		return data['image_url']

	def get_collection_stats(self, collection_id: str, decimals: int=2) -> Dict[str, float]:
		"""
		Gets stats for the given collection, rounds to the specified number of decimal points
		If the decimals arg is None then no values will be rounded
		"""

		data = self.get_collection_data(collection_id)
		stats = data['stats']

		if decimals is not None:
			stats = { k: round(v, decimals) for k, v in stats.items() }

		return stats

	def get_collection_stat(self, collection_id: str, stat_name: str, decimals: int=2) -> float:
		"""
		Gets a numerical stat for a single collection, returns None for invalid stat names
		"""

		stats = self.get_collection_stats(collection_id, decimals)
		return stats.get(stat_name)


	def get_floor_price(self, collection_id: str, decimals: int=2) -> float:
		"""
		Gets the collection floor price in ETH
		"""

		return self.get_collection_stat(collection_id, 'floor_price', decimals)

	def get_volume(self, collection_id: str, timeframe: VolumeTimeFrame, decimals: int=2) -> float:
		"""
		Gets the volume over the specified timeframe, returns all time volume for invalid timeframes
		"""

		stats = self.get_collection_stats(collection_id, decimals)
		volume = stats.get('total_volume')
		if timeframe == VolumeTimeFrame.DAILY:
			volume = stats.get('one_day_volume')
		elif timeframe == VolumeTimeFrame.WEEKLY:
			volume = stats.get('seven_day_volume')
		elif timeframe == VolumeTimeFrame.MONTHLY:
			volume = stats.get('thirty_day_volume')

		return volume

	def get_collection_size(self, collection_id: str) -> int:
		"""
		Gets the number of NFTs in a collection
		"""

		stats = self.get_collection_stats(collection_id)
		return int(stats.get('total_supply'))

	def get_number_of_owners(self, collection_id: str) -> int:
		"""
		Gets the number of unique owners for a collection
		"""

		stats = self.get_collection_stats(collection_id)
		return int(stats.get('num_owners'))

	# Contract methods
	def get_contract_data(self, collection_id: str, index: int=0) -> dict:
		"""
		Gets contract related data about a specific collection
		"""

		data = self.get_collection_data(collection_id)
		return data['primary_asset_contracts'][index]

	def get_contract_address(self, collection_id: str) -> str:
		"""
		Gets the smart contract defining this collection
		"""

		contract_data = self.get_contract_data(collection_id)
		return contract_data['address']

	# Asset methods
	def get_asset(self, collection_id: str, token_id: str) -> dict:
		"""
		Gets data on an asset given its collection and ID
		"""

		base_url = self.get_base_url()
		contract_addr = self.get_contract_address(collection_id)
		req = requests.get(f'{base_url}asset/{contract_addr}/{token_id}')
		return req.json()