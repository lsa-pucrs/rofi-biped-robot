$fn=30;
module bearing(dext,dint){
	difference(){
		cylinder(4,dext/2,dext/2,center=true);
		cylinder(4,dint/2,dint/2,center=true);
	}
}

bearing(9,4);
translate([15,0,0]){
	bearing(9,4);
}
translate([0,15,0]){
	bearing(9,4);
	translate([15,0,0]){
	bearing(9,4);
	}
}