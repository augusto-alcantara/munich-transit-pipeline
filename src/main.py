import logging
from db import get_connection
from repository import (
    create_users_table, 
    insert_user, 
    get_all_users, 
    # insert_order, 
    create_orders_table,
    create_orders_user_index, 
    get_total_spent_per_user, 
    get_user_orders_summary, 
    get_total_revenue, 
    get_average_order_value, 
    get_order_count_per_user, 
    get_users_with_multiple_orders,
    create_raw_transit_table,
    insert_raw_transit
    )
from ingestion import fetch_mvg_data



logging.basicConfig(level=logging.INFO)


def main():
    conn = get_connection()
    
    try:
        create_users_table(conn)
        create_orders_table(conn)
        create_orders_user_index(conn)

        insert_user(conn, "Gabriel")
        # insert_order(conn, 999, 100)

        insert_user(conn, "AfterFailure")

        data = fetch_mvg_data()

        create_raw_transit_table(conn)
        insert_raw_transit(conn, data)

        conn.commit()

    except Exception as e:
        logging.exception("Transaction failed")
        conn.rollback()
        
    finally:
        users = get_all_users(conn)
        logging.info("Users in database: %s", users)

        totals = get_total_spent_per_user(conn)
        logging.info("Total spent per user: %s", totals)

        summary = get_user_orders_summary(conn)
        logging.info("User order summary: %s", summary)

        logging.info("Total revenue: %s", get_total_revenue(conn))
        logging.info("Average order value: %s", get_average_order_value(conn))
        logging.info("Orders per user: %s", get_order_count_per_user(conn))
        logging.info("Users with multiple orders: %s", get_users_with_multiple_orders(conn))

        conn.close()

if __name__ == "__main__":
    main()


