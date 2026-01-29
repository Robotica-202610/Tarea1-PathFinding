"""
Build script to create executable files for Windows and macOS.
Uses PyInstaller to bundle the application into a standalone executable.
"""

import os
import sys
import platform
import subprocess
import shutil


def check_pyinstaller():
    """Check if PyInstaller is installed, install it if not."""
    try:
        import PyInstaller
        print("[INFO] PyInstaller is already installed.")
        return True
    except ImportError:
        print("[INFO] PyInstaller not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("[INFO] PyInstaller installed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install PyInstaller: {e}")
            return False


def get_platform_info():
    """Get current platform information."""
    system = platform.system()
    if system == "Darwin":
        return "macOS", ""
    elif system == "Windows":
        return "Windows", ".exe"
    elif system == "Linux":
        return "Linux", ""
    else:
        return system, ""


def build_executable():
    """Build the executable using PyInstaller."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Define paths
    main_script = os.path.join(script_dir, "__main__.py")
    dist_dir = os.path.join(project_root, "dist")
    build_dir = os.path.join(project_root, "build")

    platform_name, ext = get_platform_info()
    app_name = "Tarea1_Robotica"

    print(f"\n{'='*50}")
    print(f"Building executable for {platform_name}")
    print(f"{'='*50}\n")

    # PyInstaller command arguments
    pyinstaller_args = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",                          # Create a single executable
        "--name", app_name,                   # Name of the executable
        "--distpath", dist_dir,               # Output directory for the executable
        "--workpath", build_dir,              # Working directory for build files
        "--specpath", project_root,           # Where to store the .spec file
        "--clean",                            # Clean cache before building
        "--noconfirm",                        # Replace output directory without confirmation
        "--add-data", f"{os.path.join(script_dir, 'logic')}{os.pathsep}logic",  # Include logic module
        "--add-data", f"{os.path.join(script_dir, 'ui')}{os.pathsep}ui",        # Include ui module
        "--paths", script_dir,                # Add src to Python path
        main_script
    ]

    try:
        print("[INFO] Running PyInstaller...")
        subprocess.check_call(pyinstaller_args)

        executable_path = os.path.join(dist_dir, app_name + ext)

        print(f"\n{'='*50}")
        print(f"[SUCCESS] Build completed successfully!")
        print(f"Executable location: {executable_path}")
        print(f"{'='*50}\n")

        return executable_path

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed: {e}")
        return None


def run_executable(executable_path):
    """Run the built executable."""
    if not executable_path or not os.path.exists(executable_path):
        print("[ERROR] Executable not found. Cannot run.")
        return False

    print(f"\n[INFO] Running executable: {executable_path}\n")
    print("="*50)

    try:
        # Make sure the executable has run permissions on Unix systems
        if platform.system() != "Windows":
            os.chmod(executable_path, 0o755)

        # Run the executable
        subprocess.call([executable_path])
        return True

    except Exception as e:
        print(f"[ERROR] Failed to run executable: {e}")
        return False


def clean_build_artifacts():
    """Clean up build artifacts (optional)."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    build_dir = os.path.join(project_root, "build")
    spec_file = os.path.join(project_root, "Tarea1_Robotica.spec")

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        print("[INFO] Cleaned build directory.")

    if os.path.exists(spec_file):
        os.remove(spec_file)
        print("[INFO] Cleaned spec file.")


def main():
    """Main function to orchestrate the build process."""
    print("\n" + "="*50)
    print("  Tarea1 Robotica - Build Script")
    print("="*50)

    platform_name, _ = get_platform_info()
    print(f"\n[INFO] Detected platform: {platform_name}")
    print(f"[INFO] Python version: {platform.python_version()}")

    # Step 1: Check/Install PyInstaller
    if not check_pyinstaller():
        print("[ERROR] Cannot proceed without PyInstaller.")
        sys.exit(1)

    # Step 2: Build the executable
    executable_path = build_executable()

    if executable_path:
        # Step 3: Ask user if they want to run the executable
        try:
            choice = input("\nDo you want to run the executable now? (y/n): ").strip().lower()
            if choice == 'y' or choice == 'yes':
                run_executable(executable_path)
        except KeyboardInterrupt:
            print("\n[INFO] Build completed. Exiting...")
    else:
        print("[ERROR] Build failed. Please check the errors above.")
        sys.exit(1)

    # Optional: Clean build artifacts
    try:
        clean_choice = input("\nDo you want to clean build artifacts? (y/n): ").strip().lower()
        if clean_choice == 'y' or clean_choice == 'yes':
            clean_build_artifacts()
    except KeyboardInterrupt:
        print("\n[INFO] Exiting...")
    finally:
        print("\n[INFO] Build script finished.")
        sys.exit(0)

if __name__ == "__main__":
    main()
