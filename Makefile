.PHONY: fix dev frontend backend stop-frontend stop-backend
fix:
	git add .
	git commit -m "$$(git status --porcelain)"
	git push

dev:
	cd frontend && nohup yarn dev --host 0.0.0.0 > ../frontend.log &
	cd -
	cd backend && export STAGE=dev && python3 migrate.py && nohup python3 start.py > ../backend.log &
	cd -

frontend:
	cd frontend && nohup yarn dev --host 0.0.0.0 > ../frontend.log &

backend:
	cd backend && export STAGE=dev && python3 migrate.py && nohup python3 start.py > ../backend.log &

stop-frontend:
	pkill -f "frontend"

stop-backend:
	pkill -f "python3 start.py"
lint:
	pre-commit run --all-files
bootstrap:
	python3 bootstrap.py
