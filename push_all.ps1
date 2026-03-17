# Push to both remotes
Write-Host "Pushing to Hugging Face..." -ForegroundColor Green
git push origin main

Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push github main

Write-Host "Done! ✅" -ForegroundColor Green