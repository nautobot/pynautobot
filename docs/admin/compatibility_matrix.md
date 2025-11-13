# Compatibility Matrix

While that last supported version will not be strictly enforced--via the max_version setting, any issues with an updated Nautobot supported version in a minor release, will require a bug to be raised and a fix in Nautobot core to address, with no fixes expected in this SDK. Some features may not be fully available, see the release notes for when new Nautobot feature groups (such as DCIM, IPAM, Wireless, Cloud) are supported.

> Note that versions that support the major release of Nautobot are backwards compatible within the version of Nautobot. The versions for First Support version includes where new Nautobot core apps are introduced paired with the supported version of pynautobot. So 2.6.x will work with Nautobot 2.2, but errors will be returned when trying to access the `nautobot.wireless` attribute.

## Supported Versions

| pynautobot Version | Nautobot First Support Version | Nautobot Last Support Version |
| ------------------ | ------------------------------ | ----------------------------- |
| 1.0.X | 1.0.3 | 1.99.99 |
| 1.3.X | 1.4.0 | 1.99.99 |
| 2.0.X | 2.0.0 | 2.3.99 |
| 2.4.X | 2.3.0 | 2.3.99 |
| 2.5.X | 2.3.0 | 2.99.99 |
| 2.6.X | 2.4.0 | 2.99.99 |
| 3.0.X | 3.0.0 | 3.99.99 |
