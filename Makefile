.PHONY: test experiments clean

test:
	pytest -q

experiments:
	@for f in experiments/*.py; do echo "=== $$f ==="; python $$f; done

clean:
	rm -rf .pytest_cache src/*.egg-info src/pcc_bayes/__pycache__ tests/__pycache__
