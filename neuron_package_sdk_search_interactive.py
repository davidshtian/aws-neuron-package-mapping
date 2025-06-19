#!/usr/bin/env python3
"""
Interactive AWS Neuron SDK Package Search Sample

Simple interactive search tool for the Neuron SDK manifest.
"""

import json
import argparse

def load_manifest(manifest_file="n2-manifest.json"):
    """Load the manifest file"""
    with open(manifest_file, 'r') as f:
        return json.load(f)

def find_sdk_for_package_version(manifest, package_name, package_version):
    """Find which SDK version contains a specific package version"""
    for release in manifest.get("neuron_releases", []):
        for package in release.get("packages", []):
            if (package.get("name") == package_name and 
                package.get("version") == package_version):
                return {
                    "sdk_version": release.get("neuron_version"),
                    "supported_instances": package.get("supported_instances", []),
                    "supported_python_versions": package.get("supported_python_versions", [])
                }
    return None

def search_package_versions(manifest, package_name):
    """Get all versions of a package across SDK versions"""
    results = []
    for release in manifest.get("neuron_releases", []):
        for package in release.get("packages", []):
            if package.get("name") == package_name:
                results.append({
                    "sdk_version": release.get("neuron_version"),
                    "package_version": package.get("version"),
                    "supported_instances": package.get("supported_instances", []),
                    "supported_python_versions": package.get("supported_python_versions", [])
                })
    return results

def interactive_search(manifest_file):
    """Interactive search function"""
    manifest = load_manifest(manifest_file)
    
    print("AWS Neuron SDK Package Search")
    print("=" * 30)
    print(f"Using manifest: {manifest_file}")
    
    while True:
        print("\nOptions:")
        print("1. Search for specific package version")
        print("2. List all versions of a package")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            package_name = input("Enter package name (e.g., aws-neuronx-dkms): ").strip()
            package_version = input("Enter package version (e.g., 2.20.28.0): ").strip()
            
            if package_name and package_version:
                result = find_sdk_for_package_version(manifest, package_name, package_version)
                if result:
                    print(f"\n✓ Found {package_name}-{package_version}")
                    print(f"  SDK Version: {result['sdk_version']}")
                    print(f"  Supported Instances: {', '.join(result['supported_instances'])}")
                    if result['supported_python_versions']:
                        print(f"  Python Versions: {', '.join(result['supported_python_versions'])}")
                else:
                    print(f"\n✗ Package {package_name}-{package_version} not found")
            else:
                print("Please provide both package name and version.")
        
        elif choice == "2":
            package_name = input("Enter package name (e.g., torch-neuronx): ").strip()
            
            if package_name:
                versions = search_package_versions(manifest, package_name)
                if versions:
                    print(f"\nAll versions of {package_name}:")
                    for v in versions[:10]:  # Show first 10
                        instances = ', '.join(v['supported_instances']) if v['supported_instances'] else 'N/A'
                        print(f"  SDK {v['sdk_version']}: {v['package_version']} (instances: {instances})")
                    if len(versions) > 10:
                        print(f"  ... and {len(versions) - 10} more versions")
                else:
                    print(f"\n✗ Package {package_name} not found")
            else:
                print("Please provide a package name.")
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive AWS Neuron SDK Package Search")
    parser.add_argument("--file", default='n2-manifest.json', help='default=n2-manifest.json')
    args = parser.parse_args()
    
    try:
        interactive_search(args.file)
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except FileNotFoundError:
        print(f"Error: {args.file} file not found")
    except Exception as e:
        print(f"Error: {e}")
