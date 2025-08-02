from olist.product import Product

def get_products_stats(self, sellers_df=None):
        """
        Returns a DataFrame with:
        categories, num_of_categories, avg_price, total_n_orders, total_items_sold, total_sales
        columns,
        accepts a dataframe with 'seller_id' column
        """
        products_sellers_df = self.data['order_items'][['product_id', 'seller_id']]
        products_sellers_df = products_sellers_df.merge(Product().get_training_data(), on='product_id')

        if sellers_df is not None:
            products_sellers_df = products_sellers_df.merge(sellers_df['seller_id'], on='seller_id', how='inner')

        # set pandas cells with and height to fit all categories
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 0)

        products_sellers_df = products_sellers_df.groupby('seller_id').agg(
            categories=('category', lambda x: ', '.join(x.unique())),
            num_of_categories=('category', 'nunique'),
            avg_price=('price', 'mean'),
            total_n_orders=('n_orders', 'sum'),
            total_items_sold=('quantity', 'sum'),
            total_sales=('sales', 'sum'),
        )

        return products_sellers_df.reset_index()
