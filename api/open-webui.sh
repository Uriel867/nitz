curl -H 'Authorization: Bearer $OLLAMA_API_TOKEN' http://localhost:3000/api/chat/completions -H 'Content-Type: application/json' -d '{
    "model": "llama3:8b",
    "messages": [
        { 
            "role": "user",
            "content": "tell me a joke"
        }
    ]
}'