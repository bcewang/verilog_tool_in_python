// Configuration restrictions:
//   none.
/*
這個module是usbphy的最上層
有一個usb_pll負責產生8個phase的clock,
和usb_grp包起來的其他電路
*/
`timescale 1ps/1ps

module usb_phy(
////////////////////////////////////
		vbus,
		dp,
		dm,
		id,
		dut_hs_termination,
		vip_hs_termination,
//////////////////////////////////// 
		cdr_enable,
		dp_bit_hs_phy,
		dm_bit_hs_phy,
		dp_bit_fs_phy,
		dm_bit_fs_phy,
		hs_term_enable,
		tx_enable,
		speed_select,
		rpd_dm_enable,
		rpd_dp_enable,
		rpu_dm_enable,
		rpu_dp_enable,
		chrgvbus,
		dischrgvbus,
		idpullup,
		drvvbus,
////////////////////////////////////////
		clk_datarx,
		fs_bit_phy,
		hs_bit_phy,
		clk_480m_usb,
		clk_60m_usb,
		squelch,
		hs_disconnect,
		se_dp,
		se_dm,
		umtiotg_avld,
		umtiotg_iddig,
		umtiotg_sessend,
		umtiotg_vbusvld
);

/////////////////////////////////////////////////////////
	inout	vbus;
	input	cdr_enable;
    input	dp_bit_fs_phy;
    input	dm_bit_fs_phy;
    input	dp_bit_hs_phy;
    input	dm_bit_hs_phy;
    input	hs_term_enable;
    input	speed_select;
    input	rpd_dm_enable;
    input	tx_enable;
    input	rpd_dp_enable;
    input	rpu_dm_enable;
    input	rpu_dp_enable;
    input	chrgvbus;
    input	dischrgvbus;
    input	id;
    input	idpullup;
    input	drvvbus;
    input	dut_hs_termination;
/////////////////////////////////////////////////////////
	output	clk_datarx;
	output	fs_bit_phy;
	output	hs_bit_phy;
	output	clk_480m_usb;
	output	clk_60m_usb;
	output	squelch;
	output	hs_disconnect;
	output	se_dp;
	output	se_dm;
	output	umtiotg_avld;
	output	umtiotg_iddig;
	output	umtiotg_sessend;
	output	umtiotg_vbusvld;
	output	vip_hs_termination;
/////////////////////////////////////////////////////////
	inout	dp;
	inout	dm;
/////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
	wire	[7:0] clk;
/////////////////////////////////////////////////////////

usb_grp u_grp(
			.vbus(vbus),
			.cdr_enable(cdr_enable),
			.updn_sel(1'b0),
			.cdr_clk_edge_bit(1'b0),
			.dp_bit_fs_phy(dp_bit_fs_phy),
			.dm_bit_fs_phy(dm_bit_fs_phy),
			.dp_bit_hs_phy(dp_bit_hs_phy),
			.dm_bit_hs_phy(dm_bit_hs_phy),
			.hs_term_en(hs_term_enable),
			.tx_enable(tx_enable),
			.tx_speed(speed_select),
			.rpu_dm_enable(rpu_dm_enable),
			.rpu_dp_enable(rpu_dp_enable),
			.rpd_dm_enable(rpd_dm_enable),
			.rpd_dp_enable(rpd_dp_enable),
			.chrgvbus(chrgvbus),
			.dischrgvbus(dischrgvbus),
			.id(id),
			.idpullup(idpullup),
			.drvvbus(drvvbus),
			.clk480m(clk),
////////////////////////////////////
			.clk_datarx(clk_datarx),
			.fs_bit_phy(fs_bit_phy),
			.hs_bit_phy(hs_bit_phy),
			.clk_480m_usb(clk_480m_usb),
			.clk_60m_usb(clk_60m_usb),
			.squelch(squelch),
			.hs_disconnect(hs_disconnect),
			.se_dp(se_dp),
			.se_dm(se_dm),
			.avld(umtiotg_avld),
			.bvld(),
			.iddig(umtiotg_iddig),
			.sessend(umtiotg_sessend),
			.vbusvld(umtiotg_vbusvld),
			.dut_hs_termination(dut_hs_termination),
			.vip_hs_termination(vip_hs_termination),
			.dm(dm),
			.dp(dp)
		);
usb_pll u_pll(.clk(clk));

endmodule
