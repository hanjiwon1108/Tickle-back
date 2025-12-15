import langchain
import sys
import os

print(f"LangChain version: {langchain.__version__}")
print(f"LangChain file: {langchain.__file__}")
print(f"LangChain path: {langchain.__path__}")

try:
    import langchain.chains
    print("langchain.chains imported")
except ImportError as e:
    print(f"langchain.chains import failed: {e}")

# List directory of langchain package
package_dir = os.path.dirname(langchain.__file__)
print(f"Contents of {package_dir}:")
print(os.listdir(package_dir))
