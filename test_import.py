try:
    from langchain.chains import RetrievalQA
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
