// Update with your config settings.

module.exports = {
  development: {
    client: 'pg',
    connection: {
      database : 'knex_stickers',
      user : 'postgres',
      password : 'postgres'
    },
    pool: { min: 0, max: 12 }
  
  }
,
prod: {
  client: 'pg',
  connection: {
    host : 'postgres_container_knex_stickers',
    database : 'knex_stickers',
    user : 'postgres',
    password : 'postgres'
  },
  pool: { min: 1, max: 20  }

}
};
