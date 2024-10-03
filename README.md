# My Blog

## Description
This project is a blog application that uses Flask for the backend and Vue.js for the frontend. It allows users to explore articles and collections.

## Prerequisites
Before you begin, ensure you have the following installed on your machine:
- [Python](https://www.python.org/downloads/) (version 3.11.x)
- [Node.js](https://nodejs.org/) (version 14 or higher)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/lourencoerick/myblog-fsnd.git
   cd myblog-fsnd
   ```

2. **Backend Setup**
   - Navigate to the backend folder:
     ```bash
     cd backend
     ```
   - Create a `.env` file based on the example `.env.example` and add your PostgreSQL credentials, you should define the `DATABASE_URL`. 
   

3. **Install Backend Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Backend**
   ```bash
   flask run
   ```

5. **Frontend Setup**
   - Navigate to the frontend folder:
     ```bash
     cd ../frontend
     ```
   - Install frontend dependencies:
   ```bash
   npm install
   ```

   - Create a `.env` file based on the example `.env.example` and add your PostgreSQL credentials, you should define the `VITE_API_ENDPOINT`.   

6. **Run the Frontend**
   ```bash
   npm run serve
   ```

7. **Using Docker (Optional)**
   - You can also use Docker to run the application. From the root of the project, run:
   ```bash
   docker-compose up
   ```

## Contributing
Feel free to contribute! Fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
