import json
import os
from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'available': self.available
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(data['title'], data['author'], data['isbn'])
        book.available = data['available']
        return book

class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id

    def to_dict(self):
        return {
            'name': self.name,
            'member_id': self.member_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['member_id'])

class Loan:
    def __init__(self, book, member, loan_date, due_date):
        self.book = book
        self.member = member
        self.loan_date = loan_date
        self.due_date = due_date

    def to_dict(self):
        return {
            'book': self.book.to_dict(),
            'member': self.member.to_dict(),
            'loan_date': self.loan_date.isoformat(),
            'due_date': self.due_date.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        book = Book.from_dict(data['book'])
        member = Member.from_dict(data['member'])
        loan_date = datetime.fromisoformat(data['loan_date'])
        due_date = datetime.fromisoformat(data['due_date'])
        return cls(book, member, loan_date, due_date)

class LibraryManager:
    def __init__(self, books_file='books.json', members_file='members.json', loans_file='loans.json'):
        self.books_file = books_file
        self.members_file = members_file
        self.loans_file = loans_file
        self.books = self.load_books()
        self.members = self.load_members()
        self.loans = self.load_loans()

    def load_books(self):
        if os.path.exists(self.books_file):
            with open(self.books_file, 'r') as file:
                books_data = json.load(file)
                return [Book.from_dict(book) for book in books_data]
        return []

    def load_members(self):
        if os.path.exists(self.members_file):
            with open(self.members_file, 'r') as file:
                members_data = json.load(file)
                return [Member.from_dict(member) for member in members_data]
        return []

    def load_loans(self):
        if os.path.exists(self.loans_file):
            with open(self.loans_file, 'r') as file:
                loans_data = json.load(file)
                return [Loan.from_dict(loan) for loan in loans_data]
        return []

    def save_books(self):
        with open(self.books_file, 'w') as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4)

    def save_members(self):
        with open(self.members_file, 'w') as file:
            json.dump([member.to_dict() for member in self.members], file, indent=4)

    def save_loans(self):
        with open(self.loans_file, 'w') as file:
            json.dump([loan.to_dict() for loan in self.loans], file, indent=4)

    def add_book(self, title, author, isbn):
        book = Book(title, author, isbn)
        self.books.append(book)
        self.save_books()
        print(f'Livro adicionado: {book.title}')

    def add_member(self, name, member_id):
        member = Member(name, member_id)
        self.members.append(member)
        self.save_members()
        print(f'Membro adicionado: {member.name}')

    def loan_book(self, isbn, member_id):
        book = next((b for b in self.books if b.isbn == isbn and b.available), None)
        member = next((m for m in self.members if m.member_id == member_id), None)
        
        if book and member:
            loan_date = datetime.now()
            due_date = loan_date + timedelta(days=14)  # 2 semanas de empréstimo
            loan = Loan(book, member, loan_date, due_date)
            self.loans.append(loan)
            book.available = False
            self.save_loans()
            self.save_books()
            print(f'Livro {book.title} emprestado para {member.name}. Prazo de devolução: {due_date.date()}')
        else:
            print("Livro não disponível ou membro não encontrado.")

    def return_book(self, isbn):
        loan = next((l for l in self.loans if l.book.isbn == isbn and not l.book.available), None)
        if loan:
            loan.book.available = True
            self.loans.remove(loan)
            self.save_loans()
            self.save_books()
            print(f'Livro {loan.book.title} devolvido com sucesso.')
        else:
            print("Empréstimo não encontrado.")

    def list_books(self):
        if not self.books:
            print("Nenhum livro cadastrado.")
            return
        for book in self.books:
            status = "Disponível" if book.available else "Indisponível"
            print(f"{book.title} - {book.author} (ISBN: {book.isbn}) - {status}")

    def list_members(self):
        if not self.members:
            print("Nenhum membro cadastrado.")
            return
        for member in self.members:
            print(f"{member.name} (ID: {member.member_id})")

    def list_loans(self):
        if not self.loans:
            print("Nenhum empréstimo registrado.")
            return
        for loan in self.loans:
            print(f"{loan.book.title} emprestado por {loan.member.name} (De: {loan.loan_date.date()}, Até: {loan.due_date.date()})")

def main():
    manager = LibraryManager()

    while True:
        print("\nGerenciador da Biblioteca São Rafael")
        print("1. Adicionar Livro")
        print("2. Listar Livros")
        print("3. Adicionar Membro")
        print("4. Listar Membros")
        print("5. Emprestar Livro")
        print("6. Devolver Livro")
        print("7. Listar Empréstimos")
        print("8. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            title = input("Digite o título do livro: ")
            author = input("Digite o autor do livro: ")
            isbn = input("Digite o ISBN do livro: ")
            manager.add_book(title, author, isbn)
        elif choice == '2':
            manager.list_books()
        elif choice == '3':
            name = input("Digite o nome do membro: ")
            member_id = input("Digite o ID do membro: ")
            manager.add_member(name, member_id)
        elif choice == '4':
            manager.list_members()
        elif choice == '5':
            isbn = input("Digite o ISBN do livro a ser emprestado: ")
            member_id = input("Digite o ID do membro que irá pegar o livro: ")
            manager.loan_book(isbn, member_id)
        elif choice == '6':
            isbn = input("Digite o ISBN do livro a ser devolvido: ")
            manager.return_book(isbn)
        elif choice == '7':
            manager.list_loans()
        elif choice == '8':
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
