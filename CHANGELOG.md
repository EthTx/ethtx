# Changelog
All notable changes to this project will be documented in this file.

## 0.2.9 - 2021-10-13
### Changed
Removed indexes -incompatibility with macOS [#63](https://github.com/EthTx/ethtx/pull/63)

### Fixed
- **ENS** name fix. The contract name was decoded incorrectly, 
because `None` (unresolved) address value was overwriting the correct one [#63](https://github.com/EthTx/ethtx/pull/63)


## 0.2.8 - 2021-10-12
### Changed
- Refactored semantic providers [#59](https://github.com/EthTx/ethtx/pull/59)
- `Signatures` collection in **mongo** is now indexed [#60](https://github.com/EthTx/ethtx/pull/60)

### Fixed
- Fixed unknown args for empty guessed functions (empty arguments have been removed) [#59](https://github.com/EthTx/ethtx/pull/59)

### Added 
- Added more types [#59](https://github.com/EthTx/ethtx/pull/59)
- Added missing `__init__` files for semantics [#59](https://github.com/EthTx/ethtx/pull/59)


## 0.2.7 - 2021-10-08
### Fixed
- Fixed `ENS.fromWeb3` with poa. **ENS** did not copy middleware from injected **Web3**,
  therefore the transaction could not be decoded correctly for chains: `Goerli` and `Rinkeby` [#56](https://github.com/EthTx/ethtx/pull/56)
- Fix bug where `get_proxies` was using only default chain, instead of provided one  [#57](https://github.com/EthTx/ethtx/pull/57)


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
- All known signatures (from contracts or external sources) are stored into the database [#50](https://github.com/EthTx/ethtx/pull/50)
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




