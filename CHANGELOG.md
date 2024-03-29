# Changelog
All notable changes to [SHIS](https://github.com/nikhilweee/shis) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Addded
- This CHANGELOG file to keep track of changes.
- A *watch* feature to continuously update the website based on filesystem changes.
- A *selection* mode to select multiple file names and copy them to the clipboard - useful for filtering images.
- Two icons on each image to open the image in gallery view and in new tab respectively.
- Numbering on each image, representing the index of the image in the folder.
- The ability to group images together, essentially serving as a visual aid.

### Changed
- Switched from `Pillow` to `imagesize` for faster determination if image sizes.
- SHIS will also clean up before exiting if the `-c` option is passed.
- Moved from absolute URLs to relative URLs in the generated site.
- Switched to dynamic versioning using `setuptools-git-versioning`

### Fixed
- A bug in determining the images that have changed and need to be processed again.
- Thumbnails are now resized according to the smallest dim so images with large aspect ratios don't appear blurry.
- A bug in determining public IPs in the first run.



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