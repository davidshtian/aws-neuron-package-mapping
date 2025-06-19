# AWS Neuron Packages SDK Version Mapping
Search and mapping AWS Neuron software packages to Neuron SDK version.

## 🎯 Usage Examples

### **Interactive Search**
```
# Use default manifest
python neuron_package_sdk_search_interactive.py

# Use custom manifest file
python neuron_package_sdk_search_interactive.py --file /path/to/custom-manifest.json
```

### **CLI Search**
```
# Use default manifest
python neuron_package_sdk_search.py --package-version aws-neuronx-dkms 2.20.28.0

# Use custom manifest file
python neuron_package_sdk_search.py --file /path/to/custom-manifest.json --package-version aws-neuronx-dkms 2.20.28.0

# List all packages in SDK version 
python neuron_package_sdk_search.py --list-sdk 2.23.0

# Find all versions of torch-neuronx across all SDK versions
python neuron_package_sdk_search.py --search-package torch-neuronx

# Find torch-neuronx in SDK
python neuron_package_sdk_search.py --package-in-sdk torch-neuronx 2.23.0
```

### Manifest File
The default manifest file is from [n2-manifest.json](https://github.com/aws-neuron/aws-neuron-sdk/blob/master/src/helperscripts/n2-manifest.json).
