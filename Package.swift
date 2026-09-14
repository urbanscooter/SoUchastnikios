// swift-tools-version: 6.2

import PackageDescription

let package = Package(
    name: "SoUchastnikios",
    platforms: [.iOS(.v15)],
    targets: [
        .executableTarget(
            name: "SoUchastnikios",
            path: "Sources"
        ),
    ]
)
