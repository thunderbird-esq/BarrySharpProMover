# tests/test_example.py
import pytest

def test_basic_assertion():
    """A basic test that should always pass."""
    assert True, "Basic assertion failed"

def test_import_custom_component():
    """
    Attempts to import a module from the langflow_components package.
    This checks if the package restructuring is usable.
    """
    try:
        from langflow_components import gbstudio_build
        assert True # If import succeeds, the test part is successful
    except ImportError as e:
        pytest.fail(f"Failed to import gbstudio_build from langflow_components: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred during import: {e}")

# Example of how you might test a component if it had an importable class/function
# from langflow_components.gbstudio_build import GBStudioBuild # Assuming GBStudioBuild is a class
# def test_component_instantiation():
#     try:
#         component = GBStudioBuild() # Replace with actual instantiation if possible
#         assert component is not None
#     except Exception as e:
#         pytest.fail(f"Failed to instantiate GBStudioBuild: {e}")
