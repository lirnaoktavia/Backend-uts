from app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n=== DAFTAR ENDPOINT TERSEDIA ===")
    for rule in app.url_map.iter_rules():
        # Mengabaikan endpoint bawaan 'static' agar output lebih rapi
        if rule.endpoint != 'static':
            methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            print(f"[{methods}] http://127.0.0.1:5000{rule.rule}")
    print("================================\n")
    
    app.run(debug=True)
