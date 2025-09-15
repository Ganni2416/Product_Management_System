# client/cli.py

import argparse
import requests

API_URL = "http://127.0.0.1:5000/api/products/"

def list_products():
    res = requests.get(API_URL)
    print(res.json())

def get_product(pid):
    res = requests.get(f"{API_URL}{pid}")
    print(res.json())

def create_product(name, qty, price):
    data = {"name": name, "qty": qty, "price": price}
    res = requests.post(API_URL, json=data)
    print(res.json())

def delete_product(pid):
    res = requests.delete(f"{API_URL}{pid}")
    print("Deleted" if res.status_code == 204 else res.text)

def main():
    parser = argparse.ArgumentParser(description="PMS CLI Client")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list")

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("id", type=int)

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("name")
    create_parser.add_argument("qty", type=int)
    create_parser.add_argument("price", type=float)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)

    args = parser.parse_args()

    if args.command == "list":
        list_products()
    elif args.command == "get":
        get_product(args.id)
    elif args.command == "create":
        create_product(args.name, args.qty, args.price)
    elif args.command == "delete":
        delete_product(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
