import unittest
from typing import Optional, Union

from mhelper import BatchList, array_helper, batch_lists, string_helper, AnnotationInspector, ansi_helper, ansi


class ansi_helper_tests( unittest.TestCase ):
    def test_functions( self ):
        # TODO: These tests should check the output automatically
        
        my_text = ansi.FORE_RED + "RED" + ansi.FORE_GREEN + "GREEN" + ansi.FORE_BLUE + "BLUE" + ansi.RESET
        my_text_2 = (my_text + " ") * 20
        
        for width in (5, 10, 15):
            print( "            [" + "." * width + "]" )
            print( "fix_width = [{}]".format( ansi_helper.fix_width( my_text, width ) ) + ansi.RESET )
            print( "fix_width = [{}]".format( ansi_helper.fix_width( my_text, width, "~", -1 ) ) + ansi.RESET )
            print( "fix_width = [{}]".format( ansi_helper.fix_width( my_text, width, "~", 0 ) ) + ansi.RESET )
            print( "fix_width = [{}]".format( ansi_helper.fix_width( my_text, width, "~", 1 ) ) + ansi.RESET )
            print( "ljust     = [{}]".format( ansi_helper.ljust( my_text, width, "~" ) ) + ansi.RESET )
            print( "cjust     = [{}]".format( ansi_helper.cjust( my_text, width, "~" ) ) + ansi.RESET )
            print( "rjust     = [{}]".format( ansi_helper.rjust( my_text, width, "~" ) ) + ansi.RESET )
        
        print( "length    = [{}]".format( ansi_helper.length( my_text ) ) + ansi.RESET )
        print( "without   = [{}]".format( ansi_helper.without_ansi( my_text ) ) + ansi.RESET )
        print( "wrap20,80 = [{}]".format( "\n".join( ansi_helper.wrap( my_text_2, 80 ) ) ) + ansi.RESET )
        print( "add2      = [{}]".format( my_text + my_text ) + ansi.RESET )
        print( "multiply3 = [{}]".format( my_text * 3 ) + ansi.RESET )


class string_helper_tests( unittest.TestCase ):
    def test_highlight_quotes( self ):
        self.assertEqual( string_helper.highlight_quotes( "hello 'world' hello's", "'", "'", "<", ">" ), "hello <world> hello's" )
        self.assertEqual( string_helper.highlight_quotes( "alpha 'beta' gamma 'delta'", "'", "'", "<", ">" ), "alpha <beta> gamma <delta>" )
    
    
    def test_fix_indents( self ):
        text_a = """alpha\n\n        beta\n            gamma\n                delta\n        epsilon\n    """
        text_b = """alpha\n\nbeta\n    gamma\n        delta\nepsilon\n"""
        self.assertEqual( string_helper.fix_indents( text_a ), text_b )


class array_helper_tests( unittest.TestCase ):
    def test__create_index_lookup( self ):
        """
        TEST: create_index_lookup
        """
        
        my_list = "a", "b", "c", "d", "e"
        
        lookup = array_helper.create_index_lookup( my_list )
        
        # Sanity check
        for i, v in enumerate( my_list ):
            self.assertEqual( i, lookup[v] )


class batch_lists_test( unittest.TestCase ):
    def test__BatchList__take( self ):
        b = BatchList( (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), 3 )
        
        self.assertEqual( b.take(), [1, 2, 3] )
        self.assertEqual( b.take(), [4, 5, 6] )
        self.assertEqual( b.take(), [7, 8, 9] )
        self.assertEqual( b.take(), [10, ] )
    
    
    def test__divide_workload( self ):
        self.assertEqual( batch_lists.divide_workload( 0, 5, 51 ), (0, 10) )
        self.assertEqual( batch_lists.divide_workload( 1, 5, 51 ), (10, 20) )
        self.assertEqual( batch_lists.divide_workload( 2, 5, 51 ), (20, 30) )
        self.assertEqual( batch_lists.divide_workload( 3, 5, 51 ), (30, 40) )
        self.assertEqual( batch_lists.divide_workload( 4, 5, 51 ), (40, 51) )
    
    
    def test__divide_workload_2( self ):
        last_b = None
        for i in range( 1000 ):
            a, b = batch_lists.divide_workload( i, 1000, 1600 )
            
            self.assertGreater( b, a )
            
            if last_b is not None:
                self.assertEqual( a, last_b )
            
            last_b = b


class reflection_helper_tests( unittest.TestCase ):
    def test__annotations( self ):
        # noinspection PyClassHasNoInit
        class UPPER:
            pass
        
        
        # noinspection PyClassHasNoInit
        class MIDDLE( UPPER ):
            pass
        
        
        # noinspection PyClassHasNoInit
        class LOWER( MIDDLE ):
            pass
        
        
        # noinspection PyClassHasNoInit
        class DIFFERENT:
            pass
        
        
        self.assertTrue( AnnotationInspector( MIDDLE ).is_indirectly_below( UPPER ) )
        self.assertTrue( AnnotationInspector( Optional[MIDDLE] ).is_indirectly_below( UPPER ) )
        self.assertTrue( AnnotationInspector( Optional[Union[DIFFERENT, MIDDLE]] ).is_indirectly_below( UPPER ) )
        self.assertFalse( AnnotationInspector( Optional[Union[DIFFERENT, MIDDLE]] ).is_indirectly_below( LOWER ) )
        
        self.assertTrue( AnnotationInspector( MIDDLE ).is_directly_below( UPPER ) )
        self.assertFalse( AnnotationInspector( Optional[MIDDLE] ).is_directly_below( UPPER ) )
        
        self.assertTrue( AnnotationInspector( MIDDLE ).is_indirectly_above( LOWER ) )
        self.assertTrue( AnnotationInspector( Optional[MIDDLE] ).is_indirectly_above( LOWER ) )
        self.assertTrue( AnnotationInspector( Optional[Union[DIFFERENT, MIDDLE]] ).is_indirectly_above( LOWER ) )
        self.assertFalse( AnnotationInspector( Optional[Union[DIFFERENT, MIDDLE]] ).is_indirectly_above( UPPER ) )
        
        self.assertTrue( AnnotationInspector( MIDDLE ).is_directly_above( LOWER ) )
        self.assertFalse( AnnotationInspector( Optional[MIDDLE] ).is_directly_above( LOWER ) )
        
        middle = MIDDLE()
        
        self.assertTrue( AnnotationInspector( MIDDLE ).is_viable_instance( middle ) )
        self.assertTrue( AnnotationInspector( Optional[UPPER] ).is_viable_instance( middle ) )
        self.assertTrue( AnnotationInspector( Union[LOWER, UPPER] ).is_viable_instance( middle ) )
        self.assertFalse( AnnotationInspector( Union[LOWER] ).is_viable_instance( middle ) )


if __name__ == '__main__':
    unittest.main()
