"""The authored learning path of every IPST math topic.

Each topic lists its sets as (ปูพื้นฐาน, ฝึกคล่อง, ประยุกต์), easiest first
within a stage. The selector boosts the earliest unfinished stage, so this
order is what a learner meets: a prerequisite belongs in an earlier stage than
the sets that use it, and smaller numbers before larger ones.

Stages used to be guessed from keywords in the display name, which put, for
example, ป.5 เศษส่วนอย่างต่ำ after หารเศษส่วน. ``test_math_stages.py`` requires
every set of every IPST topic to be listed here exactly once, so a new set must
be placed by a person.

Keys omit the ``math.`` prefix.
"""

from __future__ import annotations

B = "สสวท. พื้นฐาน"
A = "สสวท. เพิ่มเติม"

Path = tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]

MATH_STAGE_PATHS: dict[tuple[str, str, str], Path] = {
    # ── ป.1 ──────────────────────────────────────────────────────────────
    (B, "ป.1", "การนับ"): (
        ("count_objects_p1", "count_kind_p1", "count_objects_20_p1"),
        ("ordinal_position_p1", "next_number", "previous_number", "number_words_p1",
         "count_bundles_p1"),
        ("thai_numerals_p1", "tens_and_ones_p1", "missing_number_in_sequence"),
    ),
    (B, "ป.1", "การบวก"): (
        ("add_pictures_p1", "one_digit_plus_no_carry"),
        ("part_whole_p1", "one_digit_plus_with_carry"),
        ("two_digit_plus", "missing_addend", "add_word_p1"),
    ),
    (B, "ป.1", "การลบ"): (
        ("subtract_pictures_p1", "one_digit_subtraction"),
        ("subtract_within_20_p1", "two_digit_subtraction_no_borrow"),
        ("two_digit_subtraction_with_borrow", "missing_subtrahend", "subtract_word_p1"),
    ),
    (B, "ป.1", "การบวกลบระคน"): (
        ("add_sub_mixed",),
        ("add_sub_mixed_missing",),
        ("add_sub_mixed_word_problem",),
    ),
    (B, "ป.1", "การเปรียบเทียบ"): (
        ("compare_groups_p1", "min_max_of_four"),
        ("true_comparison_p1", "order_numbers"),
        ("compare_who_most_p1",),
    ),
    (B, "ป.1", "แบบรูป"): (
        ("repeating_pattern_p1",),
        ("number_pattern_p1",),
        ("pattern_rule_p1", "pattern_word_p1"),
    ),
    (B, "ป.1", "โจทย์ปัญหา"): (
        ("add_word_problem", "sub_word_problem"),
        ("word_problem_number_sentence", "compare_word_problem"),
        ("missing_part_word_problem",),
    ),
    (B, "ป.1", "การวัด"): (
        ("count_units_nonstandard", "compare_nonstandard_length"),
        ("ruler_picture_p1", "compare_nonstandard_weight"),
        ("length_cm_m_p1", "weight_kg_khit_p1"),
    ),
    (B, "ป.1", "เรขาคณิต 2 มิติ"): (
        ("shape_2d_picture_p1",),
        ("classify_2d_shape",),
        ("polygon_sides",),
    ),
    (B, "ป.1", "เรขาคณิต 3 มิติ"): (
        ("classify_3d_solid",),
        ("solid_count_p1",),
        ("solid_picture_p1", "solid_objects_p1"),
    ),
    (B, "ป.1", "แผนภูมิรูปภาพ"): (
        ("pictograph_picture_p1", "pictograph_read_p1"),
        ("pictograph_compare_p1",),
        ("pictograph_most_p1",),
    ),
    # ── ป.2 ──────────────────────────────────────────────────────────────
    (B, "ป.2", "จำนวนนับไม่เกิน 1,000"): (
        ("base_ten_blocks_p2", "skip_counting", "number_reading_p2"),
        ("place_value_digit", "expanded_form_p2"),
        ("compare_sign", "order_numbers_p2"),
    ),
    (B, "ป.2", "การบวกและการลบ"): (
        ("add_columns",),
        ("sub_columns",),
        ("missing_addsub_p2", "missing_digit_p2"),
    ),
    (B, "ป.2", "การคูณ"): (
        ("multiplication_picture_p2", "repeated_addition"),
        ("multiplication_properties_p2", "multiply_1x2_p2"),
        ("multiplication_word_problem_p2",),
    ),
    (B, "ป.2", "การหาร"): (
        ("division_picture_p2", "division_facts_p2"),
        ("multiply_divide_relation_p2", "division_remainder_p2"),
        ("division_word_problem_p2",),
    ),
    (B, "ป.2", "บวก ลบ คูณ หารระคน"): (
        ("mixed_ops_p2",),
        ("mixed_ops_sentence_p2", "two_step_word_problem"),
        ("two_step_add_sub_p2", "mixed_ops_word_problem_p2"),
    ),
    (B, "ป.2", "แบบรูป"): (
        ("repeating_pattern_p2",),
        ("number_pattern_p2",),
        ("pattern_rule_p2", "pattern_word_p2"),
    ),
    (B, "ป.2", "การวัด"): (
        ("convert_length_p2", "scale_picture_p2"),
        ("convert_weight_p2", "capacity_litre_p2", "length_word_problem_p2"),
        ("weight_word_problem_p2",),
    ),
    (B, "ป.2", "รูปเรขาคณิต"): (
        ("shape_sides_picture_p2", "shape_properties_p2"),
        ("solid_shapes_p2",),
        ("shape_count_p2",),
    ),
    (B, "ป.2", "เงิน"): (
        ("money_picture_p2",),
        ("money_count_p2", "money_exchange_p2"),
        ("baht_satang_p2", "money_word_p2"),
    ),
    (B, "ป.2", "เวลา"): (
        ("clock_read_p2", "time_notation_p2"),
        ("calendar_weekday", "hours_minutes_p2"),
        ("time_to_hour", "time_elapsed"),
    ),
    (B, "ป.2", "แผนภูมิรูปภาพ"): (
        ("pictograph_key_picture_p2", "pictograph"),
        ("pictograph_compare_p2",),
        ("pictograph_symbols_p2",),
    ),
    # ── ป.3 ──────────────────────────────────────────────────────────────
    (B, "ป.3", "ค่าประจำหลัก"): (
        ("number_reading_p3",),
        ("place_value_expanded", "place_value_compose"),
        ("order_numbers_p3", "place_value_word_p3"),
    ),
    (B, "ป.3", "การคูณ"): (
        ("times_table", "multiplication"),
        ("area_model_p3", "one_digit_multiply", "multiply_2x1", "multiply_3x1_p3"),
        ("multiply_4x1_p3", "multiplication_word_problem_p3"),
    ),
    (B, "ป.3", "การหาร"): (
        ("division_remainder",),
        ("division_long", "division_check_p3"),
        ("division_word_problem_p3",),
    ),
    (B, "ป.3", "เศษส่วน"): (
        ("fraction_picture_p3", "read_fraction"),
        ("fraction_of_group_p3", "compare_fractions_p3", "like_fractions_addsub"),
        ("equivalent_fraction", "fraction_word_problem_p3"),
    ),
    (B, "ป.3", "แบบรูป"): (
        ("number_pattern_p3",),
        ("pattern_rule_p3", "growing_pattern_picture_p3"),
        ("growing_pattern_p3",),
    ),
    (B, "ป.3", "โจทย์ปัญหาระคน"): (
        ("mixed_ops_p3",),
        ("two_step_sentence_p3",),
        ("two_step_word_problem_p3",),
    ),
    (B, "ป.3", "การบวกและการลบ"): (
        ("add_sub_large_p3",),
        ("missing_addsub_large_p3",),
        ("addsub_word_large_p3",),
    ),
    (B, "ป.3", "การวัด"): (
        ("measuring_tool_p3", "estimate_measure_p3", "convert_length_p3"),
        ("convert_weight_p3", "metric_ton_p3", "length_word_problem_p3"),
        ("weight_word_problem_p3",),
    ),
    (B, "ป.3", "ปริมาตรและความจุ"): (
        ("jug_picture_p3", "convert_volume_p3"),
        ("kitchen_measures_p3",),
        ("capacity_word_problem_p3",),
    ),
    (B, "ป.3", "รูปสมมาตร"): (
        ("symmetry_picture_p3", "symmetry_axes"),
        ("symmetry_letter",),
        ("symmetry_regular_polygon", "symmetry_word_p3"),
    ),
    (B, "ป.3", "เงิน"): (
        ("baht_satang_p3", "money_total"),
        ("change_picture_p3", "income_expense_record_p3"),
        ("make_change", "money_change_left"),
    ),
    (B, "ป.3", "เวลา"): (
        ("clock_24h_p3",),
        ("duration_p3", "clock_duration_p3"),
        ("time_word_problem_p3",),
    ),
    (B, "ป.3", "ตารางทางเดียว"): (
        ("table_most_p3",),
        ("table_read_p3", "pictograph_make_p3", "tally_to_table_p3"),
        ("table_sum",),
    ),
    # ── ป.4 ──────────────────────────────────────────────────────────────
    (B, "ป.4", "ค่าประจำหลัก"): (
        ("number_reading_p4",),
        ("place_value_millions_p4",),
        ("compare_large_numbers_p4", "place_value_word_p4"),
    ),
    (B, "ป.4", "การคูณยาว"): (
        ("multiply_by_tens",),
        ("multiply_3x1", "multiply_partial_products_p4"),
        ("multiply_2x2", "multiply_multistep_p4"),
    ),
    (B, "ป.4", "การหาร"): (
        ("division",),
        ("division_2digit",),
        ("division_context_p4",),
    ),
    (B, "ป.4", "การประมาณค่า"): (
        ("rounding",),
        ("estimate_sum", "estimate_product"),
        ("estimate_word_problem_p4",),
    ),
    (B, "ป.4", "การบวกและการลบ"): (
        ("add_sub_large_p4",),
        ("missing_addsub_large_p4",),
        ("addsub_word_large_p4",),
    ),
    (B, "ป.4", "โจทย์ปัญหาระคน"): (
        ("mixed_ops_p4",),
        ("two_step_sentence_p4", "story_for_sentence_p4"),
        ("two_step_word_problem_p4",),
    ),
    (B, "ป.4", "เศษส่วน"): (
        ("fraction_bars_p4", "fraction_kinds_p4", "improper_mixed_p4"),
        ("compare_fractions_multiple_p4", "fraction_addsub_multiple_p4"),
        ("fraction_word_problem_p4",),
    ),
    (B, "ป.4", "ทศนิยม"): (
        ("decimal_grid_p4", "decimal_reading_p4", "decimal_place_value"),
        ("decimal_compare_p4", "decimal_addsub_p4"),
        ("decimal_word_problem_p4", "decimal_two_step_word_p4"),
    ),
    (B, "ป.4", "เวลา"): (
        ("time_units_p4",),
        ("calendar_word_problem_p4",),
        ("travel_time_p4",),
    ),
    (B, "ป.4", "เส้นตรงและมุม"): (
        ("classify_line", "line_ray_picture_p4", "classify_angle", "angle_kind_picture_p4", "name_angle_p4"),
        ("protractor_read_p4", "construct_angle_protractor_p4", "angle_complement_supplement"),
        ("angles_around_point_p4", "clock_angle_p4"),
    ),
    (B, "ป.4", "สี่เหลี่ยมมุมฉาก"): (
        ("rectangle_figure_p4", "rectangle_area_perimeter"),
        ("rectangle_missing_side_p4", "construct_rectangle_p4"),
        ("rectangle_word_problem_p4",),
    ),
    (B, "ป.4", "การนำเสนอข้อมูล"): (
        ("two_way_table_read_p5",),
        ("two_way_table_total_p5",),
        ("two_way_table_compare_p5",),
    ),
    (B, "ป.4", "แผนภูมิแท่ง"): (
        ("bar_chart_picture_p4", "bar_chart_read_p4"),
        ("bar_chart_diff",),
        ("bar_chart_compare_p4",),
    ),
    # ── ป.5 ──────────────────────────────────────────────────────────────
    (B, "ป.5", "เศษส่วน"): (
        ("reduce_fraction", "improper_to_mixed", "order_fractions"),
        ("add_fractions", "sub_fractions", "add_mixed_numbers"),
        ("mul_fractions", "div_fractions", "mixed_fractions", "fraction_remaining_p5"),
    ),
    (B, "ป.5", "โจทย์ปัญหาเศษส่วน"): (
        ("fraction_of_amount_p5",),
        ("fraction_word_addsub_p5",),
        ("fraction_word_muldiv_p5",),
    ),
    (B, "ป.5", "ทศนิยม"): (
        ("compare_decimals", "decimal_times_power_of_ten"),
        ("fraction_to_decimal_p5", "decimal_multiply_p5"),
        ("decimal_divide_p5", "decimal_word_problem_p5"),
    ),
    (B, "ป.5", "บัญญัติไตรยางศ์"): (
        ("unit_price_p5",),
        ("rate_word_problem_p5",),
        ("recipe_scaling_p5",),
    ),
    (B, "ป.5", "ร้อยละ"): (
        ("percent_grid_p5", "percent_of_number"),
        ("find_percent_p5", "percent_of_quantity_p5"),
        ("discount", "percent_two_step_p5"),
    ),
    (B, "ป.5", "เส้นขนาน"): (
        ("parallel_pair_picture_p5",),
        ("parallel_angle_picture_p5",),
        ("parallel_angles",),
    ),
    (B, "ป.5", "ชนิดของรูปสี่เหลี่ยม"): (
        ("quadrilateral_picture_p5", "classify_quadrilateral"),
        ("parallelogram_properties", "construct_quadrilateral_p5"),
        ("quadrilateral_angle",),
    ),
    (B, "ป.5", "พื้นที่รูปสี่เหลี่ยม"): (
        ("parallelogram_area", "parallelogram_perimeter_p5"),
        ("quadrilateral_area_figure_p5", "trapezoid_area"),
        ("rhombus_kite_area_p5",),
    ),
    (B, "ป.5", "ปริมาตร"): (
        ("unit_cubes_p5", "rectangular_prism_volume"),
        ("cube_units_p5",),
        ("volume_capacity_p5",),
    ),
    (B, "ป.5", "การนำเสนอข้อมูล"): (
        ("line_graph_picture_p5",),
        ("line_graph_change", "bar_chart_make_p5"),
        ("line_graph_problem_p5",),
    ),
    (B, "ป.5", "ปริซึม"): (
        ("prism_parts_p5",),
        ("prism_name_p5",),
        ("prism_counts_p5",),
    ),
    (B, "ป.5", "ความยาวและน้ำหนัก"): (
        ("length_decimal_p5",),
        ("weight_decimal_p5",),
        ("measure_decimal_word_p5",),
    ),
    # ── ป.6 ──────────────────────────────────────────────────────────────
    (B, "ป.6", "จำนวนเฉพาะ"): (
        ("factors_p6", "prime_or_composite"),
        ("pick_prime",),
        ("smallest_prime_factor", "prime_word_p6"),
    ),
    (B, "ป.6", "ห.ร.ม. และ ค.ร.น."): (
        ("gcd", "lcm"),
        ("gcd_word_problem_p6", "lcm_word"),
        ("gcd_lcm_relation_p6", "gcd_lcm_three_p6"),
    ),
    (B, "ป.6", "ลำดับการดำเนินการ"): (
        ("order_of_ops_integers",),
        ("order_of_ops_powers",),
        ("order_of_ops", "order_of_ops_word_p6"),
    ),
    (B, "ป.6", "ทศนิยม"): (
        ("fraction_to_decimal",),
        ("decimal_to_fraction", "divide_decimal_by_decimal_p6"),
        ("decimal_ops", "decimal_word_problem_p6", "decimal_three_step_word_p6"),
    ),
    (B, "ป.6", "ร้อยละ"): (
        ("ratio_to_percent", "percent_to_ratio"),
        ("profit_loss_p6", "simple_interest"),
        ("percent_change_p6",),
    ),
    (B, "ป.6", "อัตราส่วนและมาตราส่วน"): (
        ("write_ratio_p6", "equivalent_ratio_p6"),
        ("map_scale", "ratio_word_problem_p6"),
        ("ratio_share_p6",),
    ),
    (B, "ป.6", "แบบรูป"): (
        ("pattern_nth_term_p6",),
        ("pattern_rule_expression_p6",),
        ("matchstick_pattern_p6",),
    ),
    (B, "ป.6", "ชนิดของรูปสามเหลี่ยม"): (
        ("triangle_type_picture_p6",),
        ("classify_triangle_by_angle", "construct_triangle_p6"),
        ("triangle_missing_angle",),
    ),
    (B, "ป.6", "พื้นที่รูปสามเหลี่ยม"): (
        ("triangle_area_figure_p6", "triangle_area"),
        ("triangle_missing_side_p6", "composite_area_p6"),
        ("composite_area_figure_p6", "triangle_area_word_p6"),
    ),
    (B, "ป.6", "วงกลม"): (
        ("circle_parts",),
        ("circle_area_circumference",),
        ("circle_radius_from_circumference", "circle_word_problem_p6"),
    ),
    (B, "ป.6", "เศษส่วนและจำนวนคละ"): (
        ("order_mixed_numbers_p6",),
        ("mixed_number_ops_p6",),
        ("fraction_multistep_word_p6",),
    ),
    (B, "ป.6", "รูปเรขาคณิต 3 มิติ"): (
        ("solid_counts_picture_p6",),
        ("solid_faces_edges_vertices", "net_to_solid_p6"),
        ("euler_formula",),
    ),
    (B, "ป.6", "ปริมาตรและพื้นที่ผิว"): (
        ("prism_volume", "cube_surface_area"),
        ("composite_box_volume_p6",),
        ("water_level_p6",),
    ),
    (B, "ป.6", "แผนภูมิรูปวงกลม"): (
        ("pie_chart_picture_p6", "pie_chart"),
        ("pie_chart_amount_p6",),
        ("pie_chart_missing_p6",),
    ),
    # ── ม.1 ──────────────────────────────────────────────────────────────
    (B, "ม.1", "จำนวนเต็ม"): (
        ("number_line_picture_m1", "integer_distance_m1"),
        ("integer_addsub", "integer_muldiv"),
        ("integer_four_ops", "integer_word_problem_m1"),
    ),
    (B, "ม.1", "เลขยกกำลัง"): (
        ("power_of_2", "power_of_negative", "zero_exponent"),
        ("product_rule", "power_rule", "scientific_to_decimal", "scientific_notation",
         "scientific_compare_m1"),
        ("scientific_multiply", "scientific_notation_word_m1"),
    ),
    (B, "ม.1", "แยกตัวประกอบเฉพาะ"): (
        ("factor_tree_m1", "prime_factorization"),
        ("count_divisors",),
        ("largest_prime_factor", "prime_factor_word_m1"),
    ),
    (B, "ม.1", "จำนวนตรรกยะ"): (
        ("fraction_number_line_m1", "largest_rational"),
        ("signed_fraction_muldiv",),
        ("signed_fraction_ops", "signed_number_context_m1"),
    ),
    (B, "ม.1", "ทศนิยมและเศษส่วน"): (
        ("terminating_or_repeating_m1",),
        ("signed_decimal_ops_m1",),
        ("repeating_decimal_to_fraction_m1",),
    ),
    (B, "ม.1", "นิพจน์พีชคณิต"): (
        ("evaluate_expression",),
        ("evaluate_two_variables",),
        ("simplify_linear", "expression_word_m1"),
    ),
    (B, "ม.1", "สมการเชิงเส้น"): (
        ("balance_equation_m1", "linear_equation"),
        ("linear_equation_both_sides", "linear_equation_brackets"),
        ("linear_equation_setup_m1", "linear_word_problem_m1"),
    ),
    (B, "ม.1", "อัตราส่วนและสัดส่วน"): (
        ("simplify_ratio", "solve_proportion"),
        ("three_term_ratio_m1", "proportion_word_problem_m1"),
        ("percent_word_problem_m1",),
    ),
    (B, "ม.1", "กราฟความสัมพันธ์เชิงเส้น"): (
        ("linear_graph_read_m1", "linear_graph_point"),
        ("linear_relation_context_m1",),
        ("table_to_linear_equation_m1",),
    ),
    (B, "ม.1", "การสร้างทางเรขาคณิต"): (
        ("angle_bisector",),
        ("angle_bisector_measure",),
        ("perpendicular_bisector", "construct_angle_m1"),
    ),
    (B, "ม.1", "มิติสัมพันธ์ของรูปเรขาคณิต"): (
        ("cross_section_m1", "net_picture_m1"),
        ("solid_nets_m1",),
        ("cube_stack_m1",),
    ),
    (B, "ม.1", "สถิติ"): (
        ("double_bar_chart_m1", "frequency_table_m1", "mode_from_data"),
        ("mean_from_data",),
        ("mean_missing_value_m1",),
    ),
    # ── ม.2 ──────────────────────────────────────────────────────────────
    (B, "ม.2", "จำนวนจริง"): (
        ("nth_root", "classify_real_number"),
        ("roots_of_perfect_powers_m2", "pick_irrational", "sqrt_between_integers",
         "square_root_context_m2"),
        ("simplify_sqrt", "sqrt_product", "sqrt_measure_context_m2"),
    ),
    (B, "ม.2", "เลขยกกำลัง"): (
        ("power_of_product", "power_of_quotient", "negative_exponent",
         "negative_exponent_evaluate"),
        ("negative_exponent_simplify", "hard_product_with_negative",
         "hard_product_then_power", "hard_quotient_then_power", "hard_power_then_negative",
         "missing_exponent_m2"),
        ("fractional_exponent", "fractional_exponent_evaluate", "radical_to_exponent"),
    ),
    (B, "ม.2", "เอกนามและพหุนาม"): (
        ("classify_monomial_polynomial", "monomial_coefficient_degree",
         "monomial_like_addsub", "negate_polynomial", "combine_like_terms"),
        ("polynomial_addsub", "polynomial_addsub_quadratic", "monomial_product",
         "monomial_times_polynomial", "negative_monomial_times_polynomial"),
        ("monomial_quotient", "simplify_polynomial", "polynomial_div_monomial",
         "distribute_and_simplify", "polynomial_area_m2"),
    ),
    (B, "ม.2", "การแยกตัวประกอบของพหุนามดีกรีสอง"): (
        ("factor_common_m2",),
        ("factor_trinomial_m2",),
        ("factor_apply_m2",),
    ),
    (B, "ม.2", "แก้สมการหลายตัวแปร"): (
        ("literal_equation",),
        ("literal_equation_linear",),
        ("literal_equation_area", "formula_context_m2"),
    ),
    (B, "ม.2", "ฟังก์ชันเชิงเส้น"): (
        ("linear_function_graph_m2",),
        ("linear_function",),
        ("linear_function_from_table", "linear_model_compare_m2"),
    ),
    (B, "ม.2", "ทฤษฎีบทพีทาโกรัส"): (
        ("pythagoras", "pythagoras_figure_m2"),
        ("pythagoras_triple_check", "pythagoras_diagonal"),
        ("pythagoras_grid_distance_m2", "pythagoras_word_problem_m2"),
    ),
    (B, "ม.2", "การแปลงทางเรขาคณิต"): (
        ("reflect_point", "translate_point"),
        ("coordinate_transform",),
        ("transformation_picture_m2",),
    ),
    (B, "ม.2", "ความเท่ากันทุกประการ"): (
        ("congruence_case",),
        ("congruent_sides", "congruence_picture_m2"),
        ("congruent_angles",),
    ),
    (B, "ม.2", "เส้นขนาน"): (
        ("cointerior_angle",),
        ("transversal_picture_m2", "polygon_angle_sum"),
        ("transversal_angle_chain",),
    ),
    (B, "ม.2", "การให้เหตุผลทางเรขาคณิต"): (
        ("construct_angle_m2", "isosceles_triangle_angle_m2"),
        ("exterior_angle_m2",),
        ("converse_statement_m2",),
    ),
    (B, "ม.2", "พื้นที่ผิวและปริมาตร"): (
        ("prism_surface_area_m2", "cylinder_volume"),
        ("cylinder_surface_area_m2",),
        ("prism_cylinder_volume_word_m2",),
    ),
    (B, "ม.2", "สถิติ"): (
        ("dot_plot_picture_m2", "dot_plot_m2", "central_tendency"),
        ("stem_and_leaf_m2", "histogram_picture_m2", "median_from_data"),
        ("grouped_frequency_m2",),
    ),
    # ── ม.3 ──────────────────────────────────────────────────────────────
    (B, "ม.3", "อสมการเชิงเส้น"): (
        ("inequality",),
        ("inequality_negative_coefficient", "inequality_setup_m3"),
        ("inequality_compound", "inequality_word_problem_m3", "inequality_order_properties_m3"),
    ),
    (B, "ม.3", "กระจายทวินาม"): (
        ("expand_binomials",),
        ("expand_formula",),
        ("expand_three_terms",),
    ),
    (B, "ม.3", "แยกตัวประกอบ"): (
        ("factor_special",),
        ("factor_quadratic", "factor_cubic_common_m3"),
        ("factor_common_then_quadratic", "factor_cubic_grouping_m3"),
    ),
    (B, "ม.3", "กำลังสองสมบูรณ์"): (
        ("complete_square_constant",),
        ("quadratic_vertex",),
        ("vertex_form_convert", "vertex_context_m3"),
    ),
    (B, "ม.3", "สมการกำลังสอง"): (
        ("quadratic_equation",),
        ("quadratic_formula_roots", "quadratic_sum_product_roots", "quadratic_discriminant_m3"),
        ("quadratic_word_problem_m3",),
    ),
    (B, "ม.3", "กราฟของฟังก์ชันกำลังสอง"): (
        ("parabola_graph_m3",),
        ("parabola_vertex",),
        ("parabola_axis_intercept",),
    ),
    (B, "ม.3", "ระบบสมการ"): (
        ("simultaneous_2var", "system_substitution"),
        ("system_setup_m3",),
        ("system_word_problem",),
    ),
    (B, "ม.3", "ความคล้าย"): (
        ("similar_triangle_picture_m3", "similar_triangle"),
        ("similar_shadow", "similar_figures_ratio_m3"),
        ("similar_ratio_area",),
    ),
    (B, "ม.3", "อัตราส่วนตรีโกณมิติ"): (
        ("trig_special_values_m3", "trig_ratio_from_triple"),
        ("special_triangle_picture_m3", "trig_application_height"),
        ("trig_word_problem_m3",),
    ),
    (B, "ม.3", "วงกลม"): (
        ("central_inscribed_angle", "inscribed_angle_semicircle"),
        ("cyclic_quadrilateral", "circle_angle_picture_m3"),
        ("tangent_picture_m3", "tangent_length_m3"),
    ),
    (B, "ม.3", "พื้นที่ผิวและปริมาตร"): (
        ("pyramid_volume_m3", "cone_volume"),
        ("sphere_volume", "cone_sphere_surface_area_m3"),
        ("solid_word_problem_m3",),
    ),
    (B, "ม.3", "สถิติ (แผนภาพกล่อง)"): (
        ("box_plot_picture_m2",),
        ("box_plot_summary_m3", "boxplot_iqr"),
        ("box_plot_compare_m2",),
    ),
    (B, "ม.3", "ความน่าจะเป็นเบื้องต้น"): (
        ("probability_die_coin_m3",),
        ("spinner_probability_m3", "probability_bag_m3"),
        ("probability_two_events_m3",),
    ),
    # ── ม.4–ม.6 พื้นฐาน ────────────────────────────────────────────────────
    (B, "ม.4", "เซต"): (
        ("set_operations", "set_expression_eval_m4"),
        ("venn_picture_m4", "count_subsets", "set_expression_match_m4", "set_always_true_m4",
         "set_multiples_count_m4"),
        ("set_cardinality", "three_set_counting_m4", "set_two_set_word_m4", "set_exactly_k_m4",
         "set_region_algebra_m4", "set_extremal_m4"),
    ),
    (B, "ม.4", "ตรรกศาสตร์"): (
        ("truth_value", "logic_compound_value_m4", "proposition_identify_m4"),
        ("logic_negation", "quantifier_truth_m4", "logic_quantifier_finite_m4",
         "logic_deduce_values_m4", "logic_verbal_deduction_m4"),
        ("logic_equivalence_m4", "valid_argument", "logic_tautology_m4",
         "logic_custom_connective_m4"),
    ),
    (B, "ม.4", "หลักการนับเบื้องต้น"): (
        ("add_or_multiply_m4",),
        ("arrange_in_row_m4",),
        ("choose_group_m4",),
    ),
    (B, "ม.4", "ความน่าจะเป็นของเหตุการณ์"): (
        ("sample_space_m4",),
        ("event_probability_m4",),
        ("probability_by_choosing_m4",),
    ),
    (B, "ม.5", "จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง"): (
        ("radical_to_power_m5", "rational_power_evaluate_m5"),
        ("simplify_radicals_m5", "root_sign_properties_m5"),
        ("power_laws_rational_m5", "rational_power_context_m5", "power_compare_m5"),
    ),
    (B, "ม.5", "ฟังก์ชันในชีวิตจริง"): (
        ("function_model_type_m5",),
        ("function_context_value_m5",),
        ("function_interpret_m5",),
    ),
    (B, "ม.5", "ดอกเบี้ยและมูลค่าของเงิน"): (
        ("simple_interest_years_m5",),
        ("future_present_value_m5",),
        ("compare_offers_m5", "interest_plan_m5"),
    ),
    (B, "ม.5", "ลำดับและอนุกรม"): (
        ("arithmetic_sequence_word_m5",),
        ("geometric_sequence_word_m5", "compound_interest_m5"),
        ("present_value_m5", "regular_saving_m5", "loan_instalment_m5", "compounding_periods_m5"),
    ),
    (B, "ม.6", "การนำเสนอข้อมูลเชิงปริมาณ"): (
        ("class_boundaries_m6",),
        ("relative_frequency_m6",),
        ("cumulative_frequency_m6",),
    ),
    (B, "ม.6", "ค่ากลางของข้อมูล"): (
        ("choose_average_m6", "mean_frequency_table_m6"),
        ("weighted_mean_m6",),
        ("median_mode_frequency_m6", "mean_word_m6", "stats_data_conditions_m6"),
    ),
    (B, "ม.6", "การวัดตำแหน่งข้อมูล"): (
        ("box_plot_picture_m6", "quartile"),
        ("percentile_position",),
        ("percentile_rank_m6",),
    ),
    (B, "ม.6", "การวัดการกระจาย"): (
        ("range_of_data",),
        ("variance", "standard_deviation"),
        ("coefficient_of_variation_m6", "stats_transform_m6"),
    ),
    (B, "ม.6", "ค่ามาตรฐาน"): (
        ("z_score", "z_score_from_value"),
        ("z_score_compare",),
        ("z_score_word_m6",),
    ),
    (B, "ม.6", "การวิเคราะห์การถดถอย"): (
        ("regression_correlation", "scatter_plot_picture_m6"),
        ("linear_regression", "regression_predict_m6"),
        ("regression_slope",),
    ),
    (B, "ม.6", "สถิติประยุกต์"): (
        ("data_type_classify",),
        ("classify_data_type",),
        ("measurement_scale",),
    ),
    # ── สสวท. เพิ่มเติม ────────────────────────────────────────────────────
    (A, "ม.4", "สมการและอสมการเศษส่วน"): (
        ("rational_equation_m4",),
        ("rational_equation_extraneous_m4",),
        ("rational_inequality_m4", "partial_fractions_m4"),
    ),
    (A, "ม.4", "จัดรูปกรณฑ์"): (
        ("radical_arithmetic",),
        ("rationalize", "radical_true_statement_m4"),
        ("rationalize_binomial", "radical_geometry_m4", "radical_denest_m4", "radical_equation_m4"),
    ),
    (A, "ม.4", "ความสัมพันธ์และฟังก์ชัน"): (
        ("is_function",),
        ("function_domain", "exponential_function_m4", "function_arithmetic_m4",
         "relation_pairs_m4", "piecewise_function_m4"),
        ("function_range_linear", "cost_revenue_function_m4", "graph_inequality_parameters_m4"),
    ),
    (A, "ม.4", "ฟังก์ชันประกอบ"): (
        ("composite_evaluate",),
        ("composite_function",),
        ("composite_formula", "composite_context_m4"),
    ),
    (A, "ม.4", "สมการเลขชี้กำลัง"): (
        ("exponential_equation",),
        ("exponential_equation_same_base",),
        ("exponential_growth_word", "exponential_equation_advanced_m4"),
    ),
    (A, "ม.4", "ค่าสัมบูรณ์"): (
        ("absolute_value_evaluate",),
        ("absolute_value_equation", "absolute_value_graph_m4", "absolute_value_multi_equation_m4"),
        ("absolute_value_inequality", "absolute_value_integer_count_m4", "absolute_value_properties_m4"),
    ),
    (A, "ม.4", "การหารพหุนาม"): (
        ("remainder_theorem",),
        ("polynomial_division",),
        ("synthetic_division", "polynomial_equation_m4", "polynomial_inequality_m4",
         "polynomial_unknown_coefficients_m4", "polynomial_long_division_m4", "remainder_arithmetic_m4"),
    ),
    (A, "ม.4", "แยกตัวประกอบ"): (
        ("factor_by_grouping",),
        ("factor_cubes",),
        ("factor_advanced",),
    ),
    (A, "ม.4", "ดิสคริมิแนนต์"): (
        ("discriminant",),
        ("discriminant_k",),
        ("quadratic_complex",),
    ),
    (A, "ม.4", "ความสัมพันธ์ราก-สัมประสิทธิ์"): (
        ("vieta",),
        ("vieta_build",),
        ("vieta_expressions",),
    ),
    (A, "ม.4", "อสมการกำลังสอง"): (
        ("quadratic_inequality_sign", "quadratic_inequality_graph_m4"),
        ("quadratic_inequality", "inequality_integer_count_m4"),
        ("quadratic_inequality_interval", "quadratic_inequality_word_m4", "inequality_parameters_m4"),
    ),
    (A, "ม.4", "หาสมการพาราโบลา"): (
        ("determine_quadratic",),
        ("parabola_from_roots_m4",),
        ("parabola_three_points_m4",),
    ),
    (A, "ม.4", "เรนจ์ของฟังก์ชันกำลังสอง"): (
        ("quadratic_max_min_word",),
        ("quadratic_range_open_interval",),
        ("quadratic_range",),
    ),
    (A, "ม.4", "ฟังก์ชัน"): (
        ("inverse_function_value_m4",),
        ("inverse_function_formula_m4",),
        ("graph_shift_m4", "graph_transform_point_m4"),
    ),
    (A, "ม.4", "ลอการิทึม"): (
        ("logarithm", "log_change_of_base"),
        ("log_laws", "exp_log_graph_m4", "exp_log_graph_picture_m4", "log_mixed_bases_m5"),
        ("log_equation", "logarithm_application_m4", "log_equation_advanced_m5", "log_inequality_m5"),
    ),
    (A, "ม.4", "ระยะทาง"): (
        ("distance_between_points",),
        ("midpoint",),
        ("distance_from_origin",),
    ),
    (A, "ม.4", "เรขาคณิตวิเคราะห์"): (
        ("slope_between_points", "slope_from_equation"),
        ("parallel_perpendicular_slope",),
        ("triangle_area_coordinates_m4",),
    ),
    (A, "ม.4", "สมการเส้นตรง"): (
        ("line_intercepts", "line_equation"),
        ("line_from_two_points_intercept",),
        ("point_line_distance_m4", "line_closest_point_m4"),
    ),
    (A, "ม.4", "สมการวงกลม"): (
        ("circle_centre_radius",),
        ("circle_equation", "circle_graph_picture_m4"),
        ("circle_from_centre_point", "circle_tangency_m4"),
    ),
    (A, "ม.4", "ภาคตัดกรวย"): (
        ("conic_graph_picture_m4",),
        ("parabola_conic_m4", "ellipse_m4", "conic_general_form_m4"),
        ("hyperbola_m4", "conic_focal_definition_m4"),
    ),
    (A, "ม.5", "หลักการนับ"): (
        ("multiplication_principle",),
        ("counting_menu", "counting_complement_m5"),
        ("counting_with_restriction", "coloring_regions_m5", "stars_bars_m5"),
    ),
    (A, "ม.5", "การเรียงสับเปลี่ยน"): (
        ("permutations", "permutation_nPr"),
        ("permutation_with_repetition", "permutation_identical_m5"),
        ("circular_permutation_m5", "permutation_conditions_m5", "arrangement_blocks_gaps_m5"),
    ),
    (A, "ม.5", "การจัดหมู่"): (
        ("order_matters_m5", "combinations"),
        ("combination_identity", "combination_word_m5"),
        ("combination_committee", "distribute_to_groups_m5"),
    ),
    (A, "ม.5", "ความน่าจะเป็น"): (
        ("simple_probability", "probability_complement", "probability_two_way_table_m5"),
        ("probability_marbles", "probability_two_dice", "probability",
         "probability_union_m5", "probability_digit_numbers_m5"),
        ("probability_independent", "probability_counting_m5",
         "probability_without_replacement_m5", "probability_random_arrangement_m5",
         "probability_grid_route_m5"),
    ),
    (A, "ม.5", "อัตราส่วนตรีโกณมิติ"): (
        ("trig_ratio", "right_triangle_ratio_picture_m5"),
        ("trig_ratio_triangle_m5", "right_triangle_relations_m5"),
        ("angle_of_elevation_m5", "two_angle_height_m5"),
    ),
    (A, "ม.5", "ฟังก์ชันตรีโกณมิติ"): (
        ("unit_circle_quadrant_sign", "reference_angle", "unit_circle_picture_m5"),
        ("trig_unit_circle", "trig_graph_m5", "trig_radian_arc_m5", "trig_reduction_m5"),
        ("sine_graph_picture_m5", "trig_sum_formula_m5", "trig_identity_reduce_m5", "trig_product_sum_m5"),
    ),
    (A, "ม.5", "ตัวผกผันของฟังก์ชันตรีโกณมิติ"): (
        ("inverse_trig",),
        ("inverse_trig_range",),
        ("inverse_trig_negative", "inverse_trig_sum_m5"),
    ),
    (A, "ม.5", "สมการตรีโกณมิติ"): (
        ("trig_equation",),
        ("trig_equation_general",),
        ("trig_equation_tangent", "trig_equation_count_m5"),
    ),
    (A, "ม.5", "กฎของไซน์"): (
        ("triangle_area_sine_m5",),
        ("sine_rule_side_m5",),
        ("sine_rule_angle_m5",),
    ),
    (A, "ม.5", "กฎของโคไซน์"): (
        ("cosine_rule_side",),
        ("cosine_rule", "cosine_rule_picture_m5"),
        ("cosine_rule_angle", "cosine_rule_distance_m5", "triangle_side_type_m5"),
    ),
    (A, "ม.5", "เมทริกซ์"): (
        ("matrix_add_scalar", "matrix_transpose_m5"),
        ("matrix_multiply_2x2", "determinant_2x2", "determinant_properties_m5"),
        ("matrix_inverse_m5", "determinant_3x3_m5", "cramer_rule_m5", "matrix_row_operations_m5",
         "matrix_system_word_m5", "matrix_unique_solution_m5", "matrix_equation_m5", "matrix_power_cycle_m5"),
    ),
    (A, "ม.5", "เวกเตอร์"): (
        ("vector_add", "vector_magnitude", "vector_grid_picture_m5"),
        ("vectors", "vector_dot_product_m5", "vector_points_m5"),
        ("vector_cross_product_m5", "vector_resultant_word_m5", "vector_triple_product_m5", "vector_identity_m5"),
    ),
    (A, "ม.5", "จำนวนเชิงซ้อน"): (
        ("complex_add_conjugate", "complex_power_cycle_m5"),
        ("complex_multiply", "complex_modulus", "complex_equation_parts_m5", "complex_modulus_rules_m5"),
        ("complex_polar_m5", "complex_nth_roots_m5", "complex_conjugate_root_m5", "complex_polynomial_solve_m5"),
    ),
    (A, "ม.5", "ทฤษฎีบททวินาม"): (
        ("binomial_coefficient",),
        ("binomial_term",),
        ("binomial_middle_coefficient", "binomial_apply_m5"),
    ),
    (A, "ม.5", "ค่าคาดหมาย"): (
        ("expected_value_dice",),
        ("expected_value",),
        ("expected_value_table", "expected_value_game_m5"),
    ),
    (A, "ม.6", "ลำดับเลขคณิต"): (
        ("arithmetic_nth_term", "sequence_terms_m6"),
        ("arithmetic_sequence",),
        ("arithmetic_series_sum", "arithmetic_series_word_m6", "arithmetic_series_tricks_m6", "sequence_patterns_m6"),
    ),
    (A, "ม.6", "ลำดับเรขาคณิต"): (
        ("geometric_sequence",),
        ("geometric_nth_term",),
        ("geometric_series_finite", "geometric_series_word_m6", "geometric_series_tricks_m6"),
    ),
    (A, "ม.6", "อนุกรม"): (
        ("series_converges",),
        ("infinite_geometric_series",),
        ("repeating_decimal_to_fraction", "infinite_series_word_m6", "telescoping_series_m6", "sigma_sums_m6"),
    ),
    (A, "ม.6", "ลิมิต"): (
        ("limit_graph_picture_m6", "limit"),
        ("sequence_limit_m6",),
        ("piecewise_limit_m6",),
    ),
    (A, "ม.6", "อนุพันธ์"): (
        ("derivative_poly", "derivative_evaluate_point"),
        ("derivative_negative_power", "derivative_chain_m5"),
        ("derivative_transcendental", "motion_derivative_m6", "derivative_inverse_product_m6"),
    ),
    (A, "ม.6", "เส้นสัมผัส"): (
        ("tangent_line",),
        ("horizontal_tangent",),
        ("normal_line", "tangent_conditions_m6"),
    ),
    (A, "ม.6", "ค่าสูงสุด-ต่ำสุดสัมพัทธ์"): (
        ("derivative_sign_picture_m6", "turning_point_m5"),
        ("extrema",),
        ("optimization_word_m6", "optimization_geometry_m6", "cubic_critical_points_m6"),
    ),
    (A, "ม.6", "อินทิกรัลจำกัดเขต"): (
        ("integral_properties_m5",),
        ("definite_integral",),
        ("integral_distance_m5", "integral_accumulation_m6"),
    ),
    (A, "ม.6", "อินทิเกรตโดยการแทนค่า"): (
        ("substitution_setup_m6",),
        ("integral_substitution",),
        ("substitution_definite_m6",),
    ),
    (A, "ม.6", "อินทิเกรตทีละส่วน"): (
        ("parts_choose_u",),
        ("integration_by_parts",),
        ("parts_x_exponential",),
    ),
    (A, "ม.6", "พื้นที่"): (
        ("area_power_curve_m5",),
        ("area_under_curve",),
        ("area_between_curve_and_line", "parabola_area_m6"),
    ),
    (A, "ม.6", "พื้นที่ระหว่างเส้นโค้ง"): (
        ("area_integral_setup_m6",),
        ("area_two_curves_m6", "area_region_picture_m6"),
        ("area_between_curves",),
    ),
    (A, "ม.6", "การแจกแจงความน่าจะเป็น"): (
        ("uniform_distribution_m6", "binomial_mean_variance_m6", "random_variable_variance_m6"),
        ("binomial_probability_m6", "normal_curve_picture_m6", "expected_game_value_m6"),
        ("normal_distribution_m6", "normal_z_table_m6"),
    ),
}


def stage_of() -> dict[str, int]:
    """``math.<key>`` -> stage 1, 2 or 3."""
    return {
        f"math.{key}": stage
        for path in MATH_STAGE_PATHS.values()
        for stage, keys in enumerate(path, start=1)
        for key in keys
    }
