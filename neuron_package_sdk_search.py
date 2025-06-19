#!/usr/bin/env python3
"""
AWS Neuron SDK Package Search Tool

This script helps search through the Neuron SDK manifest to find:
- Which SDK version contains a specific package version
- All packages in a specific SDK version
- Package compatibility across instances and Python versions
"""

import json
import argparse
import sys
from typing import List, Dict, Any, Optional

class NeuronSDKSearch:
    def __init__(self, manifest_file: str = "n2-manifest.json"):
        """Initialize with manifest file"""
        try:
            with open(manifest_file, 'r') as f:
                self.manifest = json.load(f)
        except FileNotFoundError:
            print(f"Error: Manifest file '{manifest_file}' not found")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in manifest file '{manifest_file}'")
            sys.exit(1)
    
    def find_package_version(self, package_name: str, package_version: str) -> List[Dict[str, Any]]:
        """Find which SDK versions contain a specific package version"""
        results = []
        
        for release in self.manifest.get("neuron_releases", []):
            sdk_version = release.get("neuron_version")
            
            for package in release.get("packages", []):
                if (package.get("name") == package_name and 
                    package.get("version") == package_version):
                    
                    results.append({
                        "sdk_version": sdk_version,
                        "package_name": package_name,
                        "package_version": package_version,
                        "supported_instances": package.get("supported_instances", []),
                        "supported_python_versions": package.get("supported_python_versions", [])
                    })
        
        return results
    
    def find_package_in_sdk(self, package_name: str, sdk_version: str) -> List[Dict[str, Any]]:
        """Find all versions of a package in a specific SDK version"""
        results = []
        
        for release in self.manifest.get("neuron_releases", []):
            if release.get("neuron_version") == sdk_version:
                for package in release.get("packages", []):
                    if package.get("name") == package_name:
                        results.append({
                            "sdk_version": sdk_version,
                            "package_name": package_name,
                            "package_version": package.get("version"),
                            "supported_instances": package.get("supported_instances", []),
                            "supported_python_versions": package.get("supported_python_versions", [])
                        })
        
        return results
    
    def list_sdk_packages(self, sdk_version: str) -> List[Dict[str, Any]]:
        """List all packages in a specific SDK version"""
        results = []
        
        for release in self.manifest.get("neuron_releases", []):
            if release.get("neuron_version") == sdk_version:
                for package in release.get("packages", []):
                    results.append({
                        "package_name": package.get("name"),
                        "package_version": package.get("version"),
                        "supported_instances": package.get("supported_instances", []),
                        "supported_python_versions": package.get("supported_python_versions", [])
                    })
        
        return results
    
    def search_package_name(self, package_name: str) -> List[Dict[str, Any]]:
        """Search for all versions of a package across all SDK versions"""
        results = []
        
        for release in self.manifest.get("neuron_releases", []):
            sdk_version = release.get("neuron_version")
            
            for package in release.get("packages", []):
                if package.get("name") == package_name:
                    results.append({
                        "sdk_version": sdk_version,
                        "package_name": package_name,
                        "package_version": package.get("version"),
                        "supported_instances": package.get("supported_instances", []),
                        "supported_python_versions": package.get("supported_python_versions", [])
                    })
        
        return results
    
    def get_latest_sdk_versions(self) -> List[str]:
        """Get list of available SDK versions"""
        return [release.get("neuron_version") for release in self.manifest.get("neuron_releases", [])]
    
    def print_results(self, results: List[Dict[str, Any]], title: str):
        """Pretty print search results"""
        print(f"\n{title}")
        print("=" * len(title))
        
        if not results:
            print("No results found.")
            return
        
        for result in results:
            print(f"\nSDK Version: {result.get('sdk_version', 'N/A')}")
            print(f"Package: {result.get('package_name', 'N/A')}")
            print(f"Version: {result.get('package_version', 'N/A')}")
            
            instances = result.get('supported_instances', [])
            if instances:
                print(f"Supported Instances: {', '.join(instances)}")
            
            python_versions = result.get('supported_python_versions', [])
            if python_versions:
                print(f"Supported Python Versions: {', '.join(python_versions)}")
            
            print("-" * 50)

def main():
    parser = argparse.ArgumentParser(
        description="Search AWS Neuron SDK manifest for package information",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find which SDK version contains aws-neuronx-dkms-2.20.28.0
  python neuron_sdk_search.py --package-version aws-neuronx-dkms 2.20.28.0
  
  # List all packages in SDK version 2.22.0
  python neuron_sdk_search.py --list-sdk 2.22.0
  
  # Find all versions of torch-neuronx across all SDK versions
  python neuron_sdk_search.py --search-package torch-neuronx
  
  # Find torch-neuronx in SDK 2.23.0
  python neuron_sdk_search.py --package-in-sdk torch-neuronx 2.23.0
        """
    )
    
    parser.add_argument("--file", default='n2-manifest.json', help='default=n2-manifest.json')
    
    # Search options
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument("--package-version", "-pv", nargs=2, metavar=("PACKAGE", "VERSION"),
                      help="Find SDK version containing specific package version")
    
    group.add_argument("--package-in-sdk", "-ps", nargs=2, metavar=("PACKAGE", "SDK_VERSION"),
                      help="Find package versions in specific SDK version")
    
    group.add_argument("--list-sdk", "-ls", metavar="SDK_VERSION",
                      help="List all packages in SDK version")
    
    group.add_argument("--search-package", "-sp", metavar="PACKAGE",
                      help="Search for all versions of a package")
    
    group.add_argument("--list-versions", "-lv", action="store_true",
                      help="List all available SDK versions")
    
    args = parser.parse_args()
    
    # Initialize search tool
    searcher = NeuronSDKSearch(args.file)
    
    # Execute search based on arguments
    if args.package_version:
        package_name, package_version = args.package_version
        results = searcher.find_package_version(package_name, package_version)
        searcher.print_results(results, f"SDK versions containing {package_name}-{package_version}")
    
    elif args.package_in_sdk:
        package_name, sdk_version = args.package_in_sdk
        results = searcher.find_package_in_sdk(package_name, sdk_version)
        searcher.print_results(results, f"{package_name} versions in SDK {sdk_version}")
    
    elif args.list_sdk:
        results = searcher.list_sdk_packages(args.list_sdk)
        searcher.print_results(results, f"All packages in SDK {args.list_sdk}")
    
    elif args.search_package:
        results = searcher.search_package_name(args.search_package)
        searcher.print_results(results, f"All versions of {args.search_package}")
    
    elif args.list_versions:
        versions = searcher.get_latest_sdk_versions()
        print("\nAvailable SDK Versions:")
        print("=" * 25)
        for version in versions:
            print(f"  {version}")

if __name__ == "__main__":
    main()
