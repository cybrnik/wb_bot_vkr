import aiosqlite
import asyncio


class AsyncSQLighter:
    def __init__(self, database_file):
        self.database_file = database_file
        asyncio.run(self.create_connection())

    async def create_connection(self):
        self.connection = await aiosqlite.connect(self.database_file)
        self.cursor = await self.connection.cursor()
        await self.create_users_table()

    async def create_users_table(self):
        await self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    nickname TEXT,
                                    tax_rate INT DEFAULT 0,
                                    tax_system TEXT,
                                    api_feedbacks TEXT DEFAULT 'new_user',
                                    api_statistics TEXT DEFAULT 'new_user',
                                    api_finance TEXT DEFAULT 'new_user',
                                    api_advertising TEXT DEFAULT 'new_user',
                                    cur_response TEXT,
                                    activate_responses INT DEFAULT 0,
                                    num_responses INT DEFAULT 0,
                                    pattern1 TEXT,
                                    pattern2 TEXT,
                                    pattern3 TEXT,
                                    pattern4 TEXT,
                                    pattern5 TEXT,
                                    reg_date TEXT
                                  )''')

        await self.connection.commit()

    async def set_patterns(self, user_id, pattern_rate, pattern):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET {pattern_rate} = ? WHERE id = ?", (pattern, user_id))
                await connection.commit()

    async def get_pattern(self, user_id, pattern_rate):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT {pattern_rate} from users WHERE id = ? ", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def set_activate_responses(self, user_id, active):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET activate_responses = ? WHERE id = ?", (active, user_id))
                await connection.commit()

    async def get_activate_responses(self, user_id):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"SELECT activate_responses from users WHERE id = ? ", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def get_response_type(self, user_id):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT cur_response from users WHERE id = ?", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def set_response_type(self, user_id, type):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET cur_response = ? WHERE id = ?", (type, user_id))
                await connection.commit()

    async def add_user(self, user_id, username):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                if not await cursor.fetchone():
                    await cursor.execute("INSERT INTO users (id, nickname) VALUES (?, ?)", [user_id, username])
                    await connection.commit()

    async def set_api_feedbacks(self, user_id, key):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE users SET api_feedbacks = ? WHERE id = ?", (key, user_id))
                await connection.commit()

    async def get_api_feedbacks(self, user_id):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT api_feedbacks from users WHERE id = ?", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def set_api_advertising(self, user_id, key):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE users SET api_advertising = ? WHERE id = ?", (key, user_id))
                await connection.commit()

    async def get_api_advertising(self, user_id):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT api_advertising from users WHERE id = ?", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def add_response_type(self, user_id, type):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE users SET cur_response = ? WHERE id = ?", (type, user_id))
                await connection.commit()

    async def get_num_responses(self, user_id):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT num_responses from users WHERE id = ?", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def set_num_responses(self, user_id, num_responses):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET num_responses = ? WHERE id = ?", (num_responses, user_id))
                await connection.commit()

    async def get_reg_date(self, user_id):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT reg_date from users WHERE id = ?", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def set_reg_date(self, user_id, reg_date):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(f"UPDATE users SET reg_date = ? WHERE id = ?", (reg_date, user_id))
                await connection.commit()

    async def get_apis_and_patterns(self):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    "SELECT api_feedbacks, cur_response, pattern1, pattern2, pattern3, pattern4, pattern5, id, reg_date, activate_responses from users")
                result = await cursor.fetchall()
                return result

    async def get_all_statistics_api(self):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    "SELECT api_statistics, id from users")
                result = await cursor.fetchall()
                return result

    async def get_statistics_api(self, user_id):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT api_statistics from users WHERE id = ?", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def set_statistics_api(self, user_id, key):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE users SET api_statistics = ? WHERE id = ?", (key, user_id))
                await connection.commit()

    async def set_finance_api(self, user_id, key):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE users SET api_finance = ? WHERE id = ?", (key, user_id))
                await connection.commit()

    async def get_finance_api(self, user_id):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT api_finance from users WHERE id = ?", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def get_tax_rate(self, user_id):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT tax_rate from users WHERE id = ?", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def set_tax_rate(self, user_id, tax_rate):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE users SET tax_rate = ? WHERE id = ?", (tax_rate, user_id))
                await connection.commit()

    async def get_tax_system(self, user_id):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT tax_system from users WHERE id = ?", (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def set_tax_system(self, user_id, tax_system):
        async with aiosqlite.connect(self.database_file) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE users SET tax_system = ? WHERE id = ?", (tax_system, user_id))
                await connection.commit()


    async def close(self):
        await self.connection.close()


users_db = AsyncSQLighter('users.db')
