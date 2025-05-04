import subprocess


def run_migrations():
    result = subprocess.run(["alembic", "upgrade", "head"])
    if result.returncode != 0:
        raise RuntimeError("Alembic migrations failed")






if __name__ == "__main__":
    print("🚀 Running Alembic migrations...")
    run_migrations()
    print("✅ Migrations complete.")
