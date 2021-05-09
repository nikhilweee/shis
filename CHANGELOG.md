# Changelog
All notable changes to [SHIS](https://github.com/nikhilweee/shis) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Addded
- This CHANGELOG file to keep track of changes.
- A `watch` feature to continuously update the website based on filesystem changes.
- The capability to select files manually and copy selected filenames to the clipboard.

### Changed
- Switched from `Pillow` to `imagesize` for faster determination if image sizes.

### Fixed
- A bug in determining the images that have changed and need to be processed again.



## [0.1.0] - 2021-01-06
### Added
- The ability to automatically choose the next available port for starting a server.
- A [demo](https://nikhilweee.github.io/shis) hosted on GitHub pages.
- The ability to display the public IP of the machine if available.
- The ability to sort image files by `name`, or in `random` order.

### Changed
- The description bar format to handle large numbers.
- HTTP server protocol updated to HTTP/1.1.

### Fixed
- A bug in calculating the number of images that are to be processed.

[Unreleased]: https://github.com/nikhilweee/shis/compare/v0.1...HEAD
[0.1.0]: https://github.com/nikhilweee/shis/releases/tag/v0.1