# Changelog
All notable changes to this project will be documented in this file.

## 0.2.6 - 2021-10-06
### Changed
- Updated usages and project description in readme
- Ethtx now fails completely when any part of decoding fails.
- Refactored **Etherscan** provider. [#50](https://github.com/EthTx/ethtx/pull/50)
- Removed useless logs. [#50](https://github.com/EthTx/ethtx/pull/50)

### Fixed
- Changed transaction model from `TransactionMetadata` to `DecodedTransactionMetadata`
- Fixed recording of used semantics during decoding
- Fixed small PyLint issues. [#50](https://github.com/EthTx/ethtx/pull/50)
- `EthTxDecoders.get_proxies` method was missing `chain_id` parameter. [#54](https://github.com/EthTx/ethtx/pull/54)

### Added
- Added missing functions for NodeProvider interface
- From now, we try to retrieve the missing signatures from external sources: `4byte.directory`. In functions, we guess names and argument types, while in events - due to their specification, we only guess the event name. [#50](https://github.com/EthTx/ethtx/pull/50)
- The **Web3** provider is extended with **ENS** resolver. If ENS domain is available, it will be resolved to the name, example: `foo.eth`. [#50](https://github.com/EthTx/ethtx/pull/50)
- All known signatures (from contracts or external sources) are stored into the database. [#50](https://github.com/EthTx/ethtx/pull/50)
- New providers: ENS, Signature. [#50](https://github.com/EthTx/ethtx/pull/50)
- Added more types. [#50](https://github.com/EthTx/ethtx/pull/50)


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




