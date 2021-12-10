def catch_exception(origin_func):
    def wrapper(self, *args, **kwargs):
        try:
            u = origin_func(self, *args, **kwargs)
            return u
        except Exception as e:
            if hasattr( self, 'deal' ) and callable( self.deal ):
                self.deal(e)
            else:
                raise e
            return 'an Exception raised.'
    return wrapper

       
if __name__ == "__main__": 
    class B_job():
        @catch_exception
        def run(self):
            print ('aa')
            raise RuntimeError('testError')
            
        def deal(self,e):
            print ('deal')
            print (e)
    b = B_job()
    b.run()
