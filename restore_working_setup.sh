#!/bin/bash

# Open-SAS Working Setup Restore Script
# This script restores the working Jupyter notebook configuration

echo "🔄 Restoring Open-SAS Working Setup..."

# Navigate to the project directory
cd "/Users/rs255/My Technologies/Open-SAS"

# Uninstall existing kernel
echo "📦 Uninstalling existing kernel..."
python -m open_sas.kernel.install uninstall

# Install kernel
echo "📦 Installing Open-SAS kernel..."
python -m open_sas.kernel.install install

# Verify installation
echo "✅ Verifying kernel installation..."
jupyter kernelspec list

# Test kernel
echo "🧪 Testing kernel..."
python -c "
from open_sas.kernel.osas_kernel import OSASKernel
kernel = OSASKernel()
result = kernel.do_execute('data test; x=1; run;', silent=False)
print(f'Kernel test result: {result[\"status\"]}')
if result['status'] == 'ok':
    print('🎉 Kernel is working!')
else:
    print('❌ Kernel test failed')
"

echo "✅ Setup restoration complete!"
echo "📝 To use: Start Jupyter and select 'Open-SAS' kernel"
