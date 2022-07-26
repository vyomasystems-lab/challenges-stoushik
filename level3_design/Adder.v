module ha(s,ca,a,b);
	input a,b;
	output s,ca;
	xor(s,a,b);
	and(ca,a,b);
endmodule

module fa(sum,cout,a,b,cin);
	input a,b,cin;
	output sum,cout;
	wire s,c1,c2;
	ha ha1(s,c1,a,b), ha2(sum,c2,s,cin);
	or(cout,c2,c1);
endmodule

module add4(sum,a,b,cin);
	input[3:0]a,b;
	input cin;
	output[4:0]sum;
//	output
	wire [2:0]cc;
	fa a0(sum[0],cc[0],a[0],b[0],cin);
	fa a1(sum[1],cc[1],a[1],b[1],cc[0]);
	fa a2(sum[2],cc[2],a[2],b[2],cc[1]);
	fa a3(sum[3],sum[4],a[3],b[3],cc[2]);
endmodule