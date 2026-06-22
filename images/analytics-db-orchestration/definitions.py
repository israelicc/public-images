"""
Enhanced Dagster Definitions Loader - main.py Entrypoint

Supports both:
1. Single-file workflows (*.py files directly exporting assets/jobs/schedules)
2. Multi-folder projects (directories containing main.py as entrypoint)

Usage: Replace /opt/definitions.py with this file.
"""

from typing import Any

import dagster as dg
import sys
import os

dagster_jobs_dirs = [
    "/app/cronjobs",
    # "/app/dagster_jobs_host",
]

for d in dagster_jobs_dirs:
    if os.path.exists(d):
        sys.path.insert(0, d)

all_assets: list[dg.AssetsDefinition] = []
all_jobs: list[dg.JobDefinition] = []
all_schedules: list[dg.ScheduleDefinition] = []

loaded_modules: set[str] = set()


def extract_definitions(definitions_obj: dg.Definitions) -> None:
    """Extract assets, jobs, schedules from a dg.Definitions object and add to global lists."""
    if definitions_obj.assets:
        all_assets.extend(definitions_obj.assets)
    if definitions_obj.jobs:
        all_jobs.extend(definitions_obj.jobs)
    if definitions_obj.schedules:
        all_schedules.extend(definitions_obj.schedules)


def discover_and_load_definitions_attr(module: Any) -> None:
    """Discover and load dg.Definitions, assets, jobs, schedules from a module."""
    for attr_name in dir(module):
        if attr_name.startswith("_"):
            continue
        attr = getattr(module, attr_name)
        if isinstance(attr, dg.Definitions):
            extract_definitions(attr)
        elif isinstance(attr, dg.AssetsDefinition):
            all_assets.append(attr)
        elif isinstance(attr, dg.JobDefinition) or type(attr).__name__.endswith("JobDefinition"):
            all_jobs.append(attr)
        elif isinstance(attr, dg.ScheduleDefinition):
            all_schedules.append(attr)


def load_directory_project(project_dir: str, parent_dir: str) -> None:
    """
    Load a multi-folder project (directory containing main.py).
    
    Args:
        project_dir: Full path to the project directory
        parent_dir: The parent directory containing dagster_jobs
    """
    module_name = os.path.basename(project_dir)

    if module_name in loaded_modules:
        return

    main_path = os.path.join(project_dir, "main.py")
    if not os.path.exists(main_path):
        print(f"Warning: No main.py found in '{project_dir}', skipping")
        return

    current_sys_path = sys.path.copy()
    try:
        # Add project_dir to sys.path so imports like "from project.sources" work
        if project_dir not in sys.path:
            sys.path.insert(0, project_dir)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)

        # Create __init__.py if it doesn't exist (makes folder a package)
        init_path = os.path.join(project_dir, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, "w") as f:
                f.write("# Auto-generated entrypoint\nfrom .main import *\n")
            print(f"Auto-created __init__.py for {module_name}")

        # Now import works because __init__.py exists
        module = __import__(module_name)
        loaded_modules.add(module_name)
        discover_and_load_definitions_attr(module)
    except Exception as e:
        print(f"Error loading directory project '{module_name}': {e}")
    finally:
        sys.path[:] = current_sys_path


def discover_directory_projects(dagster_jobs_dir: str) -> None:
    """
    Discover all subdirectories that contain a main.py file and load them.
    
    The main.py file is the explicit entrypoint for multi-file projects.
    Skips directories starting with underscore.
    """
    if not os.path.exists(dagster_jobs_dir):
        return
    
    for entry in os.scandir(dagster_jobs_dir):
        if entry.is_dir() and not entry.name.startswith("_"):
            main_path = os.path.join(entry.path, "main.py")
            if os.path.exists(main_path):
                load_directory_project(entry.path, dagster_jobs_dir)


def load_single_file_module(filename: str, dagster_jobs_dir: str) -> None:
    """
    Load a single Python file as a Dagster module.
    
    Args:
        filename: Name of the .py file (e.g., 'my_job.py')
        dagster_jobs_dir: Directory containing the file
    """
    module_name = filename[:-3]
    
    if module_name in loaded_modules:
        return
    
    current_sys_path = sys.path.copy()
    try:
        if dagster_jobs_dir not in sys.path:
            sys.path.insert(0, dagster_jobs_dir)
        
        try:
            module = __import__(module_name)
            loaded_modules.add(module_name)
            discover_and_load_definitions_attr(module)
        except Exception as e:
            print(f"Error loading single file module '{module_name}': {e}")
    finally:
        sys.path[:] = current_sys_path


def discover_single_file_modules(dagster_jobs_dir: str) -> None:
    """Discover and load all single .py files (excluding __init__.py and files starting with _)."""
    if not os.path.exists(dagster_jobs_dir):
        return
    
    for filename in os.listdir(dagster_jobs_dir):
        if filename.endswith(".py") and not filename.startswith("_") and filename != "__init__.py":
            load_single_file_module(filename, dagster_jobs_dir)


def load_all_dagster_definitions() -> None:
    """Main loader function - discovers and loads all Dagster definitions."""
    for dagster_jobs_dir in dagster_jobs_dirs:
        if not os.path.exists(dagster_jobs_dir):
            continue
        
        discover_directory_projects(dagster_jobs_dir)
        discover_single_file_modules(dagster_jobs_dir)


load_all_dagster_definitions()

definitions = dg.Definitions(
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules,
)