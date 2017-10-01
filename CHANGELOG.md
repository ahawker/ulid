# Change Log

## [Unreleased](https://github.com/ahawker/ulid/tree/HEAD)

[Full Changelog](https://github.com/ahawker/ulid/compare/v0.0.4...HEAD)

**Merged pull requests:**

- Add Python code security linting with bandit. [\#47](https://github.com/ahawker/ulid/pull/47) ([ahawker](https://github.com/ahawker))
- Refactor security scan into separate Travis CI job. [\#46](https://github.com/ahawker/ulid/pull/46) ([ahawker](https://github.com/ahawker))
- Refactor lint checking into separate Travis CI job. [\#45](https://github.com/ahawker/ulid/pull/45) ([ahawker](https://github.com/ahawker))
- pyup.io:  Scheduled daily dependency update on saturday [\#44](https://github.com/ahawker/ulid/pull/44) ([pyup-bot](https://github.com/pyup-bot))
- pyup.io:  Scheduled daily dependency update on thursday [\#42](https://github.com/ahawker/ulid/pull/42) ([pyup-bot](https://github.com/pyup-bot))

## [v0.0.4](https://github.com/ahawker/ulid/tree/v0.0.4) (2017-09-22)
[Full Changelog](https://github.com/ahawker/ulid/compare/v0.0.3...v0.0.4)

**Implemented enhancements:**

- Add mypy support [\#25](https://github.com/ahawker/ulid/issues/25)
- Address reported pylint issues [\#22](https://github.com/ahawker/ulid/issues/22)
- Code Coverage: ulid/ulid.py [\#18](https://github.com/ahawker/ulid/issues/18)
- Code Coverage: ulid/base32.py [\#17](https://github.com/ahawker/ulid/issues/17)
- Code Coverage: ulid/api.py [\#16](https://github.com/ahawker/ulid/issues/16)
- Update README with pros/cons vs. UUID [\#4](https://github.com/ahawker/ulid/issues/4)

**Closed issues:**

- Monitor dependency versions [\#30](https://github.com/ahawker/ulid/issues/30)
- Freeze Dependency Versions [\#29](https://github.com/ahawker/ulid/issues/29)
- Remove "development" requirements from base.txt [\#28](https://github.com/ahawker/ulid/issues/28)

**Merged pull requests:**

- Switch to legacy pypi and testpypi endpoints. [\#39](https://github.com/ahawker/ulid/pull/39) ([ahawker](https://github.com/ahawker))
- Update setup.py to use restructured text documentation. [\#38](https://github.com/ahawker/ulid/pull/38) ([ahawker](https://github.com/ahawker))
- pyup.io:  Scheduled daily dependency update on tuesday [\#37](https://github.com/ahawker/ulid/pull/37) ([pyup-bot](https://github.com/pyup-bot))
- Add Safety check scans. [\#34](https://github.com/ahawker/ulid/pull/34) ([ahawker](https://github.com/ahawker))
- Add pyup.io config file. [\#32](https://github.com/ahawker/ulid/pull/32) ([ahawker](https://github.com/ahawker))
- Pin all requirements to latest versions \(if usable\). [\#31](https://github.com/ahawker/ulid/pull/31) ([ahawker](https://github.com/ahawker))
- Break dev vs. runtime requirements into separate files. [\#27](https://github.com/ahawker/ulid/pull/27) ([ahawker](https://github.com/ahawker))
- Add mypy static analysis support. [\#26](https://github.com/ahawker/ulid/pull/26) ([ahawker](https://github.com/ahawker))
- Add lint target as TravisCI script dependency. [\#24](https://github.com/ahawker/ulid/pull/24) ([ahawker](https://github.com/ahawker))
- Address pylint issues with refactoring and explicit disables. [\#23](https://github.com/ahawker/ulid/pull/23) ([ahawker](https://github.com/ahawker))
- Fix copy pasta bug in from\_randomness tests. [\#21](https://github.com/ahawker/ulid/pull/21) ([ahawker](https://github.com/ahawker))
- Add tests for Base32 decode attempts with non-ascii chars. [\#20](https://github.com/ahawker/ulid/pull/20) ([ahawker](https://github.com/ahawker))
- Add rich comparison tests for all model types not just MemoryView. [\#19](https://github.com/ahawker/ulid/pull/19) ([ahawker](https://github.com/ahawker))
- Add waffle.io badge. [\#15](https://github.com/ahawker/ulid/pull/15) ([ahawker](https://github.com/ahawker))

## [v0.0.3](https://github.com/ahawker/ulid/tree/v0.0.3) (2017-06-25)
[Full Changelog](https://github.com/ahawker/ulid/compare/v0.0.2...v0.0.3)

**Implemented enhancements:**

- Read the Docs Support [\#7](https://github.com/ahawker/ulid/issues/7)
- API: from\_randomness should support ULID/Randomness objects [\#6](https://github.com/ahawker/ulid/issues/6)
- API: from\_timestamp should support ULID/Timestamp objects. [\#5](https://github.com/ahawker/ulid/issues/5)

**Merged pull requests:**

- Update README with UUID v. ULID pros/cons. [\#14](https://github.com/ahawker/ulid/pull/14) ([ahawker](https://github.com/ahawker))
- Fix from\_X documentation for collection of supported types. [\#13](https://github.com/ahawker/ulid/pull/13) ([ahawker](https://github.com/ahawker))
- Refactor model representation methods to be properties. [\#12](https://github.com/ahawker/ulid/pull/12) ([ahawker](https://github.com/ahawker))
- Add Sphinx support for autogen API docs. [\#11](https://github.com/ahawker/ulid/pull/11) ([ahawker](https://github.com/ahawker))
- Add basic object creation tests using pytest-benchmark. [\#10](https://github.com/ahawker/ulid/pull/10) ([ahawker](https://github.com/ahawker))
- Support Randomness/ULID model types in api.from\_randomness. [\#9](https://github.com/ahawker/ulid/pull/9) ([ahawker](https://github.com/ahawker))
- Support Timestamp/ULID model types in api.from\_timestamp. [\#8](https://github.com/ahawker/ulid/pull/8) ([ahawker](https://github.com/ahawker))

## [v0.0.2](https://github.com/ahawker/ulid/tree/v0.0.2) (2017-06-16)


\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*