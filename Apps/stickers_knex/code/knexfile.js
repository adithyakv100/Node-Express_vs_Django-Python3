// Update with your config settings.

module.exports = {
  development: {
    client: 'pg',
    connection: {
      host : 'postgres_container_knex_stickers',
      database : 'knex_stickers',
      user : 'postgres',
      password : 'postgres'
    }}
,
  test: {
    client: 'pg',
    connection: 'postgres://localhost/test-cjs-web-store'
  },
  production: {
    client: 'pg',
    connection: process.env.DATABASE_URL
  }
};
