# Changelog

<!--next-version-placeholder-->

## v2.0.0 (2025-03-05)

### Feature

* Add and resolve query projection for products and specs respectively ([#97](https://github.com/ni/nisystemlink-clients-python/issues/97)) ([`e9feff6`](https://github.com/ni/nisystemlink-clients-python/commit/e9feff6dc3e473dd34cbb53739f1c96eb7a8db0e))

### Breaking

* Product and Specification models have been updated to support projections.  - Product client changes--    - `models.Product` now defines all fields as Optional.    - `ProductClient.create_product`'s `products` parameter is now typed      as `models.CreateProductRequest`    - `ProductClient.update_product`'s `products` parameter is now typed      as `models.UpdateProductRequest`  - Specifications client changes--    - `models.Specification` and `models.SpecificationDefinition` now      define all fields as Optional.    - `models.QuerySpecifications` has been renamed `models.PagedSpecifications`      to better align to other clients.    - `models.CreateSpecificationeRequest.specs` is now typed as `models.CreateSpecificationsRequestObject`      instead of `models.SpecificationDefinition`    - `models.UpdateSpecificationeRequest.specs` is now typed as `models.UpdateSpecificationsRequestObject`      instead of `models.Specification` ([`e9feff6`](https://github.com/ni/nisystemlink-clients-python/commit/e9feff6dc3e473dd34cbb53739f1c96eb7a8db0e))

## v1.10.0 (2025-02-13)

### Feature

* Example to upload file to SystemLink ([#81](https://github.com/ni/nisystemlink-clients-python/issues/81)) ([`67bfe2d`](https://github.com/ni/nisystemlink-clients-python/commit/67bfe2dc69565f744a36248cbda15026018d7ad6))

## v1.9.0 (2025-02-06)

### Feature

* Add minimal client implementation for Feeds API ([#73](https://github.com/ni/nisystemlink-clients-python/issues/73)) ([`35d32b5`](https://github.com/ni/nisystemlink-clients-python/commit/35d32b580488b1365165f8c6e0a96e8148169b1d))

## v1.8.1 (2025-02-05)

### Fix

* Update to the latest httpx version ([#88](https://github.com/ni/nisystemlink-clients-python/issues/88)) ([`09e6e59`](https://github.com/ni/nisystemlink-clients-python/commit/09e6e59e1025d0046da08dd9743d0ac3fc0872f2))

## v1.8.0 (2024-11-08)

### Feature

* Add client for SystemLink products API ([#69](https://github.com/ni/nisystemlink-clients-python/issues/69)) ([`d53a9f4`](https://github.com/ni/nisystemlink-clients-python/commit/d53a9f43aee5abbf1e9db084b091390b148478a5))

## v1.7.2 (2024-11-05)

### Fix

* Some spelling errors file tests ([#79](https://github.com/ni/nisystemlink-clients-python/issues/79)) ([`770545e`](https://github.com/ni/nisystemlink-clients-python/commit/770545e6cbb9d90d48f9633dff979cff5c71dc67))

## v1.7.1 (2024-11-04)

### Fix

* Remove SL Cloud from readme and add SLE ([#78](https://github.com/ni/nisystemlink-clients-python/issues/78)) ([`ae12825`](https://github.com/ni/nisystemlink-clients-python/commit/ae12825912ddefa871e81ca7a4e5ee16de216a9b))

## v1.7.0 (2024-10-25)

### Feature

* Add workspace field to httpconfiguration ([#64](https://github.com/ni/nisystemlink-clients-python/issues/64)) ([`b81c84a`](https://github.com/ni/nisystemlink-clients-python/commit/b81c84ada616df9cfe72e7d63e41ae17801af474))

## v1.6.0 (2024-09-17)

### Feature

* Add Client for File Service ([#65](https://github.com/ni/nisystemlink-clients-python/issues/65)) ([`ebdc4c1`](https://github.com/ni/nisystemlink-clients-python/commit/ebdc4c1adf50f71498d0ce3446402dff55eef6ca))

## v1.5.0 (2024-09-09)

### Feature

* Add client for Artifacts API ([#70](https://github.com/ni/nisystemlink-clients-python/issues/70)) ([`0ada3d7`](https://github.com/ni/nisystemlink-clients-python/commit/0ada3d7c765e1b5d7fabfa4661f15d38c71c7295))

## v1.4.3 (2024-08-08)

### Fix

* Make SpecClient() work with default values for optional args ([#68](https://github.com/ni/nisystemlink-clients-python/issues/68)) ([`fb60801`](https://github.com/ni/nisystemlink-clients-python/commit/fb60801d4093ef66c92e7b2c6e4e1f5fe45bb2f6))

## v1.4.2 (2024-07-15)

### Fix

* Bump setuptools from 67.6.0 to 70.0.0 ([#67](https://github.com/ni/nisystemlink-clients-python/issues/67)) ([`39b13f0`](https://github.com/ni/nisystemlink-clients-python/commit/39b13f0c4b3ed3377e54dd6c4a3237c7e9304e48))

## v1.4.1 (2024-07-08)

### Fix

* Bump certifi from 2023.7.22 to 2024.7.4 ([#66](https://github.com/ni/nisystemlink-clients-python/issues/66)) ([`0fc4ff7`](https://github.com/ni/nisystemlink-clients-python/commit/0fc4ff766895a70be4c0e518ba98db0e69beab43))

## v1.4.0 (2024-06-18)

### Feature

* Make DataFrame and Spec clients compatible with SystemLink Client http configuration ([#61](https://github.com/ni/nisystemlink-clients-python/issues/61)) ([`7954e14`](https://github.com/ni/nisystemlink-clients-python/commit/7954e1479a0e421cfe3e44c741e69186e2f0c45f))

## v1.3.1 (2024-05-21)

### Fix

* Bump requests from 2.31.0 to 2.32.0 ([#60](https://github.com/ni/nisystemlink-clients-python/issues/60)) ([`fe9060b`](https://github.com/ni/nisystemlink-clients-python/commit/fe9060b1783e4022cb493a96bd42bb052526c487))

## v1.3.0 (2024-04-19)

### Feature

* Test monitor API information routes client ([#57](https://github.com/ni/nisystemlink-clients-python/issues/57)) ([`4b9cc61`](https://github.com/ni/nisystemlink-clients-python/commit/4b9cc6135c0fa4d99e8c93201f83d3a17a817239))

## v1.2.1 (2024-04-12)

### Fix

* Bump idna from 3.4 to 3.7 ([#56](https://github.com/ni/nisystemlink-clients-python/issues/56)) ([`008f523`](https://github.com/ni/nisystemlink-clients-python/commit/008f523063b1c8afd559cc0d14e2199137814584))

## v1.2.0 (2024-04-04)

### Feature

* Add spec client, examples, and docs ([#53](https://github.com/ni/nisystemlink-clients-python/issues/53)) ([`7c88535`](https://github.com/ni/nisystemlink-clients-python/commit/7c8853587cbe1ae21b5039e59d3f1d125f851288))

## v1.1.2 (2023-10-03)

### Fix

* Bump urllib3 from 1.26.15 to 1.26.17 ([#49](https://github.com/ni/nisystemlink-clients-python/issues/49)) ([`8d86216`](https://github.com/ni/nisystemlink-clients-python/commit/8d86216d760bfc860a9e504b04ee62d4cada193f))

## v1.1.1 (2023-09-22)

### Fix

* Bump certifi from 2022.12.7 to 2023.7.22 ([#47](https://github.com/ni/nisystemlink-clients-python/issues/47)) ([`79f6aad`](https://github.com/ni/nisystemlink-clients-python/commit/79f6aadcbe545143051386f7fcc7b7d38613a36e))

## v1.1.0 (2023-04-06)
### Feature
* Add CSV export capability to DataFrameClient ([#45](https://github.com/ni/nisystemlink-clients-python/issues/45)) ([`5cc2d01`](https://github.com/ni/nisystemlink-clients-python/commit/5cc2d01c0655fdd8ab1d5e1895d5be38020c9cd0))

## v1.0.2 (2023-03-08)
### Fix
* Correct spelling for model class TableMetadataModification ([#44](https://github.com/ni/nisystemlink-clients-python/issues/44)) ([`30c760c`](https://github.com/ni/nisystemlink-clients-python/commit/30c760c2eb9af8e17ddb8c6730f6ef5aae20e973))

## v1.0.1 (2023-01-26)
### Fix
* Fix various documentation issues ([#42](https://github.com/ni/nisystemlink-clients-python/issues/42)) ([`872e9ac`](https://github.com/ni/nisystemlink-clients-python/commit/872e9accdc959e8fc8a400518bb74ba8fb0cf30c))

## v1.0.0 (2022-12-15)
### Breaking
* Preparation for 1.0.0 release. ([`c61925c`](https://github.com/ni/nisystemlink-clients-python/commit/c61925c902ebcdf6e1e4c8c24905caf0c304cb31))

### Documentation
* Add examples and update getting started ([#40](https://github.com/ni/nisystemlink-clients-python/issues/40)) ([`1d76480`](https://github.com/ni/nisystemlink-clients-python/commit/1d76480f6bf3eddf0017f467d68473131e4850a0))

## v0.9.0 (2022-12-06)
### Feature
* Query for data ([#37](https://github.com/ni/nisystemlink-clients-python/issues/37)) ([`7f0acbe`](https://github.com/ni/nisystemlink-clients-python/commit/7f0acbec9c9033a088259172712e9c2532594d2e))

## v0.8.0 (2022-12-05)
### Feature
* Read and append table data ([#36](https://github.com/ni/nisystemlink-clients-python/issues/36)) ([`d7a7642`](https://github.com/ni/nisystemlink-clients-python/commit/d7a7642f12543be4c1393435c9fd11604288a17f))

## v0.7.0 (2022-12-02)
### Feature
* Add modify_tables method ([#35](https://github.com/ni/nisystemlink-clients-python/issues/35)) ([`7be03be`](https://github.com/ni/nisystemlink-clients-python/commit/7be03be811d7c7d239e69883e00b765f8a316881))

## v0.6.0 (2022-12-01)
### Feature
* Table multi-delete + refactoring core libs ([#34](https://github.com/ni/nisystemlink-clients-python/issues/34)) ([`ebe9ce3`](https://github.com/ni/nisystemlink-clients-python/commit/ebe9ce3c4d6a84049d38806b2966637ca318629d))

## v0.5.0 (2022-11-30)
### Feature
* Method to update table metadata ([#33](https://github.com/ni/nisystemlink-clients-python/issues/33)) ([`6e72835`](https://github.com/ni/nisystemlink-clients-python/commit/6e7283512d9d02fed8238811247d3d0e706a2c4b))

## v0.4.0 (2022-11-28)
### Feature
* Add query-tables method ([#32](https://github.com/ni/nisystemlink-clients-python/issues/32)) ([`8b8afef`](https://github.com/ni/nisystemlink-clients-python/commit/8b8afef8ae5ccd9f93017ff3e5629d6cbeec3f58))

## v0.3.0 (2022-11-19)
### Feature
* Implement create/get/delete/list table metadata methods ([#28](https://github.com/ni/nisystemlink-clients-python/issues/28)) ([`7cbf7e8`](https://github.com/ni/nisystemlink-clients-python/commit/7cbf7e8f9f46ece55ceddd8f48f55a91c79a2e24))
