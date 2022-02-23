from pydantic import BaseSettings


class Settings(BaseSettings):
    DEFAULT_CHAIN: str = "mainnet"
    CACHE_SIZE: int = 128

    MONGO_CONNECTION_STRING: str

    WEB3_NODES: dict

    ETHERSCAN_API_KEY: str
    ETHERSCAN_URLS: dict = {
        "mainnet": "https://api.etherscan.io/api",
        "goerli": "https://api-goerli.etherscan.io/api",
        "rinkeby": "https://api-rinkeby.etherscan.io/api",
    }

    class Config:
        case_sensitive = True
        env_file = "../../.env"


EthTxConfig = Settings()
