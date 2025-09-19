
import sparrow.toolkit.route.router as rt
import sparrow.toolkit.route.slots as sl


router = rt.Router(sl.origin_address)

def test_router():

    address1 = "23 Glenlake Ave, Toronto, ON"  
    point1 = router.address_to_point(address1)
    distance, travel_time = router.distance_and_time( router.origin_point, point1 )
    print(f"Travel time: {travel_time:.3f} min", f"Distance: {distance:.3f} km")

    address2 = "1246 Yonge St, Toronto, ON"
    point2 = router.address_to_point(address2)
    distance, travel_time = router.distance_and_time( point1, point2 )
    print(f"Travel time: {travel_time:.3f} min", f"Distance: {distance:.3f} km")

    router.save_route( point1, point2 )
