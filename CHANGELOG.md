# Changelog
All notable changes to this project will be documented in this file.


## 0.3.22 - 2023-05-17

### Changed
- Bumped `web3` to ~6 and adapted code to breaking changes [#191](https://github.com/EthTx/ethtx/pull/191)
- Simplified stringification process of `Decimal` objects [#192](https://github.com/EthTx/ethtx/pull/192)


## 0.3.21 - 2022-12-01

### Fixed
- Deleted invalid cache wrapper on get_erc20_token in web3provider [#187](https://github.com/EthTx/ethtx/pull/187)


## 0.3.20 - 2022-11-25

### Changed
- Bumped `web3` to 5.28.0 and removed no longer necessary `eth` dependecies [#178](https://github.com/EthTx/ethtx/pull/178)
- Set field `DecodedEvent.value` and `DecodedTransfer.value` as Decimal [#179](https://github.com/EthTx/ethtx/pull/179)
- Removed `requests-cache` dependencies and replaced with standard `requests` [#180](https://github.com/EthTx/ethtx/pull/180)

### Fixed
- Fixed missing `decoded_value` in `parameters` of decoded events [#171](https://github.com/EthTx/ethtx/pull/171)
- Fixed `Web3ENSProviderENSProvider` resolution [#178](https://github.com/EthTx/ethtx/pull/178)
- Fixed **major issue regarding loss of decimal precision** for `value` field in decoded models `Argument`,
  `DecodedCall` and `DecodedTransfer` [#179](https://github.com/EthTx/ethtx/pull/179)


## 0.3.19 - 2022-10-06

### Fixed
- Fix output decoding for reverted calls[#172](https://github.com/EthTx/ethtx/pull/172)
- Fix missing decoded_value in parameters decoding for events [#173](https://github.com/EthTx/ethtx/pull/173)


## 0.3.18 - 2022-10-06

### Fixed
- Fixed amount calculation for NFT transfers [#169](https://github.com/EthTx/ethtx/pull/169)
- Fix decode_static_argument doubling 0x prefix in bytes type [#168](https://github.com/EthTx/ethtx/pull/168)


## 0.3.17 - 2022-07-18

### Changed
- Refactored/split `utils` code [#156](https://github.com/EthTx/ethtx/pull/156)
- Refactored `SignatureProvider` [#156](https://github.com/EthTx/ethtx/pull/156)
- Removed `@cache` from signature Cursor object [#156](https://github.com/EthTx/ethtx/pull/156)
- Updated logging [#156](https://github.com/EthTx/ethtx/pull/156)

### Fixed
- Updated `requests-cache` version. Pipenv could not handle the bad dependencies in this
  package [#157](https://github.com/EthTx/ethtx/pull/157)
- Fixed guessing function (problem with writing to and reading from the
  base) [#156](https://github.com/EthTx/ethtx/pull/156)


## 0.3.16 - 2022-05-26

### Changed
- Removed support for optional parameters in mongo, due to different tiers of
  atlas [#152](https://github.com/EthTx/ethtx/pull/152)
- Removed the formatting of `transfer.value`, so the value remains
  unchanged [#152](https://github.com/EthTx/ethtx/pull/152)
- Renamed a variable in `README.md` [#152](https://github.com/EthTx/ethtx/pull/152)
- `black` formatting [#152](https://github.com/EthTx/ethtx/pull/152)


## 0.3.15 - 2022-05-26

### Fixed
- Break dynamic array decoding if there are no more available parameter
- Fixed `DecodedTransfer.value` type (str -> float) [#144](https://github.com/EthTx/ethtx/pull/144)
- Fixed `README` mongo string [#140](https://github.com/EthTx/ethtx/pull/140)

### Changed
- Make more flexible deps - `ethtx` is easier to install in other apps [#140](https://github.com/EthTx/ethtx/pull/140)
- No timeout for mongo cursor - some collections may sometimes require more time to
  search [#140](https://github.com/EthTx/ethtx/pull/140)

### Added
- Cache `4bytes` response, if some transactions have a lot of guessed functions/events, it definitely speeds
  up `ethtx`! [#140](https://github.com/EthTx/ethtx/pull/140)
- Added an option to recreate semantics used for transaction decoding [#148](https://github.com/EthTx/ethtx/pull/148)


## 0.3.14 - 2022-04-06

### Fixed
- Caught exception for ens where there is no code associated with the specified
  address [#137](https://github.com/EthTx/ethtx/pull/137)
- Fixed wrong transaction metadata types [#136](https://github.com/EthTx/ethtx/pull/136)

### Changed
- Skip compiled structure from `4bytes` [#138](https://github.com/EthTx/ethtx/pull/138)
- Updated black `pre-commit` version [#136](https://github.com/EthTx/ethtx/pull/136)
- Updated tests [#136](https://github.com/EthTx/ethtx/pull/136)

### Added
- Added optional fields `from_address` and `to_address` to DecodedTransactionMetadata
  model [#136](https://github.com/EthTx/ethtx/pull/136)


## 0.3.13 - 2022-03-30

### Fixed
- Gracefully handle errors for evaluating value of transfers [#133](https://github.com/EthTx/ethtx/pull/133)


## 0.3.12 - 2022-03-29

### Changed
- Add placeholder names for not decoded parameters [#131](https://github.com/EthTx/ethtx/pull/131)


## 0.3.11 - 2022-03-29

### Fixes
- Fix decoding of strings with special characters [#127](https://github.com/EthTx/ethtx/pull/127)
- Fix incorrect usage of Web3.toChecksumAddress [#128](https://github.com/EthTx/ethtx/pull/128)
- Fix decoding of Transfers that use invalid ERC20/ERC721 events [#129](https://github.com/EthTx/ethtx/pull/129)


## 0.3.10 - 2022-03-03

### Added
- Added `CACHE_SIZE` environment variable used to set the size of the cache [#121](https://github.com/EthTx/ethtx/pull/121)
- Overwritten `lru_cache` decorator with custom `cache` decorator, which uses
  `CACHE_SIZE` environment variable to set the size of the cache [#121](https://github.com/EthTx/ethtx/pull/121)
- Make pydantic `BaseModel` hashable.

### Changed
- Do not update semantics every time from `ENS` [#117](https://github.com/EthTx/ethtx/pull/117)

### Fixed
- Fixed some documentation errors in `README.md` file [#121](https://github.com/EthTx/ethtx/pull/121)


## 0.3.9 - 2022-02-02

### Added
- Add some static types and LRU caches for proxy guessing and web3 [#112](https://github.com/EthTx/ethtx/pull/112)

### Changed
- Updated old ***Features*** section in `README.md` [#114](https://github.com/EthTx/ethtx/pull/114)
- Removed *requirements.txt* file. Builds will use Pipfile from now on [#114](https://github.com/EthTx/ethtx/pull/114)

### Fixed
- `to_address` field in Call/DecodedCall is optional now [#111](https://github.com/EthTx/ethtx/pull/111)
- Fixed `web3` dependencies [#114](https://github.com/EthTx/ethtx/pull/114)
- Delete bunch of invalid if conditions when checking for semantic [#113](https://github.com/EthTx/ethtx/pull/113)


## 0.3.8 - 2022-01-14
### Added
- Added option to disable refreshing of addresses in ENS for existing semantics [#106](https://github.com/EthTx/ethtx/pull/106)
- Increased and added more lru_caches in different providers [#105](https://github.com/EthTx/ethtx/pull/105)

### Changed
- Python version bumped to 3.9 [#103](https://github.com/EthTx/ethtx/pull/103)
- Deleted ethereum price field from decoded transaction model, will be moved to ethtx_ce [#104](https://github.com/EthTx/ethtx/pull/104)

### Fixed
- Fixed decoding of anonymous events without known contract's abi [#107](https://github.com/EthTx/ethtx/pull/107)


## 0.3.7 - 2021-12-24
### Changed
- Update build dev requirements [#88](https://github.com/EthTx/ethtx/pull/88)


## 0.3.6 - 2021-12-24
### Changed
- Update build requirements [#86](https://github.com/EthTx/ethtx/pull/86)


## 0.3.5 - 2021-12-24
### Changed
- Delete unused dependency on `ethereum` package, organized others [#84](https://github.com/EthTx/ethtx/pull/84)
- Make object models work with reverted events [#83](https://github.com/EthTx/ethtx/pull/83)


## 0.3.4 - 2021-12-16
### Changed
- Set field `W3CallTree.to_address` as optional [#77](https://github.com/EthTx/ethtx/pull/77)

### Fixed
- Fixed readme commas and delete unused mongo_database from example [#80](https://github.com/EthTx/ethtx/pull/80)
- Parameters decoding fixes [#81](https://github.com/EthTx/ethtx/pull/81)


## 0.3.3 - 2021-11-05
### Changed
- Return lowercase address if `ENS` provider can not resolve it to name [#75](https://github.com/EthTx/ethtx/pull/75)


## 0.3.2 - 2021-11-02
### Changed
- Changed exception `Web3ConnectionException` to `NodeConnectionException`[#68](https://github.com/EthTx/ethtx/pull/68)
- Changed `tests` directory structure [#68](https://github.com/EthTx/ethtx/pull/68)
- All models now use `pydantic` [#72](https://github.com/EthTx/ethtx/pull/72)
- Removed `jsonpickle` [#72](https://github.com/EthTx/ethtx/pull/72)
- Changed the order of methods in `DecoderService` [#72](https://github.com/EthTx/ethtx/pull/72)
- Update requirements (*requirements.txt* & *Pipfile*) [#72](https://github.com/EthTx/ethtx/pull/72)
- Update **README** [#72](https://github.com/EthTx/ethtx/pull/72)
- `strip()` every single node URL in `NodeConnectionPool` [#72](https://github.com/EthTx/ethtx/pull/72)
- Refactored ENS provider, each time a new ens object is taken [#71](https://github.com/EthTx/ethtx/pull/71)

### Fixed
- Fixed types in models [#72](https://github.com/EthTx/ethtx/pull/72)
- Fixed bug with empty args from `4byte` [#72](https://github.com/EthTx/ethtx/pull/72)

### Added
- Added node switcher - if one is unavailable, it uses the others available to connect with
  node [#68](https://github.com/EthTx/ethtx/pull/68)
- Extended function end event models [#72](https://github.com/EthTx/ethtx/pull/72)
- Model tests added [#72](https://github.com/EthTx/ethtx/pull/72)
- Catch more exceptions from `4byte.directory` (looks like the service is not always working
  properly) [#71](https://github.com/EthTx/ethtx/pull/71)
- Added more logging [#71](https://github.com/EthTx/ethtx/pull/71)
- Added more exceptions [#71](https://github.com/EthTx/ethtx/pull/71)


## 0.3.1 - 2021-10-14
### Fixed
- Fix tuple components processing [#66](https://github.com/EthTx/ethtx/pull/66)


## 0.3.0 - 2021-10-14
### Fixed
- Fixed bug where mongo was using database called 'db', instead of one specified in connection
  string [#62](https://github.com/EthTx/ethtx/pull/62)


## 0.2.9 - 2021-10-13
### Changed
- Removed indexes -incompatibility with macOS [#63](https://github.com/EthTx/ethtx/pull/63)

### Fixed
- **ENS** name fix. The contract name was decoded incorrectly, because `None` (unresolved) address value was overwriting
  the correct one [#63](https://github.com/EthTx/ethtx/pull/63)


## 0.2.8 - 2021-10-12
### Changed
- Refactored semantic providers [#59](https://github.com/EthTx/ethtx/pull/59)
- `Signatures` collection in **mongo** is now indexed [#60](https://github.com/EthTx/ethtx/pull/60)

### Fixed
- Fixed unknown args for empty guessed functions (empty arguments have been
  removed) [#59](https://github.com/EthTx/ethtx/pull/59)

### Added
- Added more types [#59](https://github.com/EthTx/ethtx/pull/59)
- Added missing `__init__` files for semantics [#59](https://github.com/EthTx/ethtx/pull/59)


## 0.2.7 - 2021-10-08
### Fixed
- Fixed `ENS.fromWeb3` with poa. **ENS** did not copy middleware from injected **Web3**, therefore the transaction could
  not be decoded correctly for chains: `Goerli` and `Rinkeby` [#56](https://github.com/EthTx/ethtx/pull/56)
- Fix bug where `get_proxies` was using only default chain, instead of provided
  one  [#57](https://github.com/EthTx/ethtx/pull/57)


## 0.2.6 - 2021-10-06
### Changed
- Refactored Etherscan provider [#50](https://github.com/EthTx/ethtx/pull/50)
- Removed useless logs [#50](https://github.com/EthTx/ethtx/pull/50)
- Ethtx now fails completely when any part of decoding fails
- Updated usages and project description in readme

### Fixed
- Fixed decoding of multidimensional arrays
- Changed transaction model from TransactionMetadata to DecodedTransactionMetadata
- Fixed recording of semantics used during decoding
- Fixed small PyLint issues [#50](https://github.com/EthTx/ethtx/pull/50)
- Added missing chain_id parameter to EthTxDecoders.get_proxies method [#54](https://github.com/EthTx/ethtx/pull/54)

### Added
- Standard Proxy contracts (e.g. EIP1969) are now properly decoded
- All known signatures (from contracts or external sources) are stored into the
  database [#50](https://github.com/EthTx/ethtx/pull/50)
- Guessing missing signatures using other contracts and 4byte.directory [#50](https://github.com/EthTx/ethtx/pull/50)
- Resolving ENS domains [#50](https://github.com/EthTx/ethtx/pull/50)
- New providers: ENS, Signature [#50](https://github.com/EthTx/ethtx/pull/50)
- Added missing functions for NodeProvider interface
- Added more types [#50](https://github.com/EthTx/ethtx/pull/50)


## 0.2.5 - 2021-09-16
### Fixed
- Fixed multidimensional arrays processing
- Fixed unnecessary semantics saving

### Changed
- Increased log level for exceptions in every decoding part and exposing more information


## 0.2.4 - 2021-08-31
### Fixed
- Increased timeout for 'debug_traceTransaction' call


## 0.2.3 - 2021-08-18
### Fixed
- Fixed Web3 requests for testnets


## 0.2.2 - 2021-08-17
### Fixed
- Proper decoding of guessed ERC20 ABI and transformations
- ERC20 and ERC721 events processing fixes
- Reading stored semantics fix
- ERC721 proxies processing fix


## 0.2.1 - 2021-08-10
### Added
- Added support for Goerli nodes

### Fixed
- Fixed return values and dynamic arrays processing
- Proper handling of block ExtraBytes for PoA chains

### Changed
- EthTxConfig object format


## 0.1.9 - 2021-08-04
### Fixed
- Added missing files, fixed broken build


## 0.1.8 - 2021-08-04
### Fixed
- fixed badges for transfers and balances
- fixed events parameters decoding

### Changed
- changed decoded models
- changed delegations processing for proxy detection

### Added
- added precompiled contracts calls processing


## 0.1.7 - 2021-07-30
### Fixed
- Delegate calls pruning fix


## 0.1.6 - 2021-07-28
### Fixed
- Fixed anonymous events processing


## 0.1.5 - 2021-07-27
### Fixed
- Fixed semantic decoding for contract creation txs

### Changed
- Changelog refactor.


## 0.1.4 - 2021-10-25
### Fixed
- Token proxies handling fixes.


## 0.1.3 - 2021-10-24
### Fixed
- ABI and semantic decoding fixes.
- Semantics repository reading fixes.


## 0.1.2 - 2021-10-21
### Changed
- Caching optimization.


## 0.1.1 - 2021-10-21
### Fixed
- README content fix.


## 0.1.0 - 2021-10-21
### Added
- Initial release.
