import pandas as pd
class DataAnalyzer:
    def __init__(self, games_file, genres_file, themes_file, platforms_file, game_engine_file):
        # read the files and set the values to member values
        self.games_df = pd.read_csv(games_file)
        self.genres_df = pd.read_csv(genres_file)
        self.themes_df = pd.read_csv(themes_file)
        self.platforms_df = pd.read_csv(platforms_file)
        self.game_engine_df = pd.read_csv(game_engine_file)
        self.pre_processing()



    def pre_processing(self):
        # Parse the 'genres' and 'themes' columns into lists
        self.games_df['genres'] = self.games_df['genres'].apply(lambda x: [int(y.strip()) for y in x[1:-1].split(',')] if pd.notnull(x) else x)
        self.games_df['themes'] = self.games_df['themes'].apply(lambda x: [int(y.strip()) for y in x[1:-1].split(',')] if pd.notnull(x) else x)
        self.games_df['platforms'] = self.games_df['platforms'].apply(lambda x: [int(y.strip()) for y in x[1:-1].split(',')] if pd.notnull(x) else x)
        self.games_df['game_engines'] = self.games_df['game_engines'].apply(lambda x: [int(y.strip()) for y in x[1:-1].split(',')] if pd.notnull(x) else x)
        # Extract release year and month from 'first_release_date'
        self.games_df['release_year'] = pd.to_datetime(self.games_df['first_release_date'], unit='s').dt.year
        self.games_df['release_month'] = pd.to_datetime(self.games_df['first_release_date'], unit='s').dt.month


    
    def count_games_per_year(self):

    # Count games per year
    # This looks so cool! 
        yearly_counts = self.games_df['release_year'].value_counts().reset_index()
        yearly_counts.columns = ['year', 'num_games']
        yearly_counts = yearly_counts.sort_values('year')

        # Drop rows with NaN years (if any)
        yearly_counts = yearly_counts.dropna(subset=['year'])
        yearly_counts['year'] = yearly_counts['year'].astype(int) # Ensure year is an integer

        return yearly_counts

    
    def count_genre_games_per_year(self):
        genre_slice = self.genres_df[['id', 'name']]
        game_slice = self.games_df[['release_year', 'genres']]

        # Explode and map genres
        games_exploded = game_slice.explode('genres')
        games_exploded = games_exploded.merge(genre_slice, left_on='genres', right_on='id', how='left')
        games_exploded = games_exploded.rename(columns={'name': 'genre_name'})

        # Group by year and genre
        genre_yearly = games_exploded.groupby(['release_year', 'genre_name']).size().reset_index(name='num_games')
        genre_yearly['num_games'] = genre_yearly['num_games'].astype(int)

        return genre_yearly
    

    def count_theme_games_per_year(self):
        theme_slice = self.themes_df[['id', 'name']]
        game_slice = self.games_df[['release_year', 'themes']]

        # Explode and map themes
       
        games_exploded = game_slice.explode('themes')
        games_exploded = games_exploded.merge(theme_slice, left_on='themes', right_on='id', how='left')
        games_exploded = games_exploded.rename(columns={'name': 'theme_name'})

        # Group by year and genre
        theme_yearly = games_exploded.groupby(['release_year', 'theme_name']).size().reset_index(name='num_games')
        theme_yearly['num_games'] = theme_yearly['num_games'].astype(int)

        return theme_yearly
    
    def count_games_per_month(self):
        # Count games per month across all years
        monthly_counts = self.games_df.groupby('release_month').size().reset_index(name='num_games')

        # Map month numbers to names for better readability
        month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
                    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        monthly_counts['month_name'] = monthly_counts['release_month'].map(month_names)

        return monthly_counts
    
    def count_platforms(self):

        platform_slice = self.platforms_df[['id', 'name']]
        platform_stats = self.games_df.explode('platforms')
        game_slice = platform_stats[['platforms']]
        platforms_with_name = game_slice.merge(platform_slice, left_on='platforms', right_on='id', how='left')
        platform_count = platforms_with_name['name'].value_counts().reset_index(name='platform_count')
        threshold = 1 * self.games_df.shape[0] / 100
        major_platforms = platform_count[platform_count['platform_count'] >= threshold]
        other_count = platform_count[platform_count['platform_count'] < threshold].sum(axis=0)['platform_count']
        labels = list(major_platforms.name) + ['Other']
        values = list(major_platforms.platform_count) + [other_count]
        platform_count = pd.DataFrame({'name': labels, 'count': values})
        return platform_count
    

    def count_game_engines(self):

        game_engine_slice = self.game_engine_df[['id', 'name']]
        game_engine_stats = self.games_df.explode('game_engines')
        game_engine_stats = game_engine_stats[['game_engines']]
        game_engine_stats = game_engine_stats.dropna()
        game_engine_count = game_engine_stats['game_engines'].value_counts().reset_index()
        game_engine_count.columns = ['id', 'count']
        print(game_engine_count.head(20))
        game_engine_count = game_engine_stats.merge(game_engine_slice, left_on='game_engines', right_on='id', how = 'left')
        game_engine_count['name'] = game_engine_count['name'].apply(
            lambda x: 'Unity' if str(x).lower().startswith('unity') else x
        )
        game_engine_count = game_engine_count['name'].value_counts().reset_index(name='count')
        threshold = 1 * game_engine_stats.shape[0] / 100
        print(threshold)
        major_engines = game_engine_count[game_engine_count['count'] >= threshold]
        # print(game_engine_count.head(20))
        other_count = game_engine_count[game_engine_count['count'] < threshold].sum(axis=0)['count']
        values = list(major_engines['count']) + [other_count]
        names = list(major_engines['name']) + ['Other']
        game_engine_count = pd.DataFrame({'name': names, 'count': values})
        print(game_engine_count.head())
        return game_engine_count

