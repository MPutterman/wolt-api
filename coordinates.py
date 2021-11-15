class Coordinates:
    def __init__(self,long,lat):
        self.lat,self.long= lat,long
    def __repr__(self):
        return f'Coordinates({self.long},{self.lat})'
    def __getitem__(self,ind):
        if ind==0:
            return self.long
        if ind ==1:
            return self.lat
        else:
            return None
    def __tuple__(self):
        return self[0],self[1]