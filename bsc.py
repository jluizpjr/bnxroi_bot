import asyncio
from bscscan import BscScan

YOUR_API_KEY = "MQF2SIVV8XZMHWGHGDYVB7C1Y7EXD8M3SM"

async def main():
  async with BscScan(YOUR_API_KEY) as bsc:
    print(await bsc.get_bnb_balance(address="0x54b6Ea430199F50dD59fE333F24b0DdD572e0B9a"))

  async with BscScan(YOUR_API_KEY) as client:
    print(
        await client.get_acc_balance_by_token_contract_address(
            contract_address="0xb3a6381070B1a15169DEA646166EC0699fDAeA79",
            address="0x54b6Ea430199F50dD59fE333F24b0DdD572e0B9a"
        )
    )

  async with BscScan(YOUR_API_KEY) as client:
    print(
        await client.get_total_supply_by_contract_address(
                contract_address="0xb3a6381070B1a15169DEA646166EC0699fDAeA79"
            )
    )

if __name__ == "__main__":
  asyncio.run(main())

