New-Item -Path "scripts/generators" -ItemType Directory -Force
New-Item -Path "scripts/utilities" -ItemType Directory -Force
New-Item -Path "scripts/migrations" -ItemType Directory -Force
New-Item -Path "scripts/verification" -ItemType Directory -Force
New-Item -Path "tests/unit" -ItemType Directory -Force
New-Item -Path "tests/integration" -ItemType Directory -Force
New-Item -Path "tests/ai" -ItemType Directory -Force
New-Item -Path "tests/infrastructure" -ItemType Directory -Force
New-Item -Path "docs" -ItemType Directory -Force

# Move generators
Move-Item "create_base.py" "scripts/generators/" -Force
Move-Item "create_bias_agent.py" "scripts/generators/" -Force
Move-Item "create_embedding_agent.py" "scripts/generators/" -Force
Move-Item "create_embedding_service.py" "scripts/generators/" -Force
Move-Item "create_evidence_agent.py" "scripts/generators/" -Force
Move-Item "create_intake_agent.py" "scripts/generators/" -Force
Move-Item "create_llm_service.py" "scripts/generators/" -Force
Move-Item "create_pipeline.py" "scripts/generators/" -Force
Move-Item "create_prompts.py" "scripts/generators/" -Force
Move-Item "create_vector_store.py" "scripts/generators/" -Force

# Move utilities
Move-Item "update_state.py" "scripts/utilities/" -Force
Move-Item "verify_state.py" "scripts/utilities/" -Force

# Move migrations
Move-Item "fix_future.py" "scripts/migrations/" -Force
Move-Item "fix_migrations.py" "scripts/migrations/" -Force

# Move AI Tests
Move-Item "test_base_agent.py" "tests/ai/" -Force
Move-Item "test_bias_agent.py" "tests/ai/" -Force
Move-Item "test_embedding_agent.py" "tests/ai/" -Force
Move-Item "test_embedding_service.py" "tests/ai/" -Force
Move-Item "test_evidence_agent.py" "tests/ai/" -Force
Move-Item "test_intake_agent.py" "tests/ai/" -Force
Move-Item "test_llm_service.py" "tests/ai/" -Force
Move-Item "test_pipeline.py" "tests/ai/" -Force
Move-Item "test_prompts.py" "tests/ai/" -Force
Move-Item "test_vector_store.py" "tests/ai/" -Force

# Move Infrastructure Tests
Move-Item "test_create.py" "tests/infrastructure/" -Force
Move-Item "test_create_pg.py" "tests/infrastructure/" -Force
Move-Item "test_enum.py" "tests/infrastructure/" -Force

# Create __init__.py files
New-Item -Path "tests/__init__.py" -ItemType File -Force
New-Item -Path "tests/ai/__init__.py" -ItemType File -Force
New-Item -Path "tests/infrastructure/__init__.py" -ItemType File -Force
New-Item -Path "tests/unit/__init__.py" -ItemType File -Force
New-Item -Path "tests/integration/__init__.py" -ItemType File -Force

