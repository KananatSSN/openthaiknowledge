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
        ("add_pictures_p1", "one_digit_plus_no_carry", "add_tens_p1", "add_commutative_p1"),
        ("part_whole_p1", "one_digit_plus_with_carry", "add_three_numbers_p1"),
        ("two_digit_plus", "missing_addend", "add_word_p1"),
    ),
    (B, "ป.1", "การลบ"): (
        ("subtract_pictures_p1", "one_digit_subtraction", "subtract_tens_p1", "number_line_back_p1"),
        ("subtract_within_20_p1", "two_digit_subtraction_no_borrow", "add_sub_inverse_p1"),
        ("two_digit_subtraction_with_borrow", "missing_subtrahend", "subtract_word_p1"),
    ),
    (B, "ป.1", "การบวกลบระคน"): (
        ("add_sub_mixed", "mixed_number_line_p1"),
        ("add_sub_mixed_missing", "mixed_four_terms_p1", "mixed_largest_p1", "mixed_true_sentence_p1"),
        ("add_sub_mixed_word_problem", "mixed_give_compare_p1", "mixed_start_amount_p1",
         "mixed_change_p1"),
    ),
    (B, "ป.1", "การเปรียบเทียบ"): (
        ("compare_groups_p1", "min_max_of_four", "more_less_than_p1", "number_between_p1"),
        ("true_comparison_p1", "order_numbers", "two_digit_from_digits_p1", "count_between_p1"),
        ("compare_who_most_p1", "sorted_position_p1"),
    ),
    (B, "ป.1", "แบบรูป"): (
        ("repeating_pattern_p1", "pattern_colours_p1", "pattern_next_term_p1"),
        ("number_pattern_p1", "pattern_nth_shape_p1", "count_down_tens_p1", "pattern_shape_count_p1"),
        ("pattern_rule_p1", "pattern_word_p1", "pattern_growing_p1"),
    ),
    (B, "ป.1", "โจทย์ปัญหา"): (
        ("add_word_problem", "sub_word_problem", "money_left_p1", "tens_bundles_word_p1"),
        ("word_problem_number_sentence", "compare_word_problem", "more_needed_p1", "age_word_p1"),
        ("missing_part_word_problem", "line_position_p1"),
    ),
    (B, "ป.1", "การวัด"): (
        ("count_units_nonstandard", "compare_nonstandard_length", "choose_unit_p1"),
        ("ruler_picture_p1", "compare_nonstandard_weight", "length_difference_p1", "join_lengths_p1"),
        ("length_cm_m_p1", "weight_kg_khit_p1", "weight_compare_kg_p1"),
    ),
    (B, "ป.1", "เรขาคณิต 2 มิติ"): (
        ("shape_2d_picture_p1", "shape_corners_p1", "shape_objects_p1", "shape_description_p1"),
        ("classify_2d_shape", "shape_total_sides_p1", "shape_sides_compare_p1", "shape_odd_one_p1"),
        ("polygon_sides", "fold_cut_shape_p1"),
    ),
    (B, "ป.1", "เรขาคณิต 3 มิติ"): (
        ("classify_3d_solid", "solid_which_object_p1", "solid_face_shape_p1"),
        ("solid_count_p1", "solid_roll_stack_p1", "solid_odd_one_p1", "solid_trace_p1"),
        ("solid_picture_p1", "solid_objects_p1", "solid_sum_p1"),
    ),
    (B, "ป.1", "แผนภูมิรูปภาพ"): (
        ("pictograph_picture_p1", "pictograph_read_p1", "pictograph_add_more_p1"),
        ("pictograph_compare_p1", "pictograph_range_p1", "pictograph_order_p1",
         "pictograph_count_above_p1"),
        ("pictograph_most_p1", "pictograph_true_statement_p1", "pictograph_two_rows_p1"),
    ),
    # ── ป.2 ──────────────────────────────────────────────────────────────
    (B, "ป.2", "จำนวนนับไม่เกิน 1,000"): (
        ("base_ten_blocks_p2", "skip_counting", "number_reading_p2", "even_number_p2",
         "hundreds_tens_ones_p2"),
        ("place_value_digit", "expanded_form_p2", "more_less_100_p2"),
        ("compare_sign", "order_numbers_p2"),
    ),
    (B, "ป.2", "การบวกและการลบ"): (
        ("add_columns", "add_three_two_digit_p2"),
        ("sub_columns", "check_with_inverse_p2", "largest_sum_p2"),
        ("missing_addsub_p2", "missing_digit_p2", "add_word_three_digit_p2", "sub_word_three_digit_p2",
         "how_many_more_p2"),
    ),
    (B, "ป.2", "การคูณ"): (
        ("multiplication_picture_p2", "repeated_addition", "times_table_p2", "multiply_zero_one_p2"),
        ("multiplication_properties_p2", "multiply_1x2_p2", "multiply_by_ten_p2", "largest_product_p2"),
        ("multiplication_word_problem_p2", "array_rows_p2"),
    ),
    (B, "ป.2", "การหาร"): (
        ("division_picture_p2", "division_facts_p2", "division_check_p2"),
        ("multiply_divide_relation_p2", "division_remainder_p2", "missing_dividend_p2",
         "fact_family_p2", "largest_quotient_p2"),
        ("division_word_problem_p2", "division_leftover_word_p2"),
    ),
    (B, "ป.2", "บวก ลบ คูณ หารระคน"): (
        ("mixed_ops_p2",),
        ("mixed_ops_sentence_p2", "two_step_word_problem", "mixed_true_sentence_p2"),
        ("two_step_add_sub_p2", "mixed_ops_word_problem_p2", "legs_count_p2", "wheels_count_p2",
         "compare_two_buys_p2", "fill_bags_left_p2"),
    ),
    (B, "ป.2", "แบบรูป"): (
        ("repeating_pattern_p2", "pattern_next_p2", "pattern_three_nth_p2"),
        ("number_pattern_p2", "pattern_two_missing_p2", "pattern_count_back_p2", "pattern_nth_term_p2"),
        ("pattern_rule_p2", "pattern_word_p2", "pattern_growing_dots_p2"),
    ),
    (B, "ป.2", "การวัด"): (
        ("convert_length_p2", "scale_picture_p2", "cm_to_m_cm_p2"),
        ("convert_weight_p2", "capacity_litre_p2", "length_word_problem_p2", "kg_g_to_g_p2",
         "longest_mixed_units_p2"),
        ("weight_word_problem_p2", "length_compare_mixed_p2"),
    ),
    (B, "ป.2", "รูปเรขาคณิต"): (
        ("shape_sides_picture_p2", "shape_properties_p2", "curved_straight_p2", "line_kinds_p2",
         "circle_ellipse_p2"),
        ("solid_shapes_p2", "solid_faces_count_p2", "count_shapes_list_p2"),
        ("shape_count_p2", "total_corners_p2"),
    ),
    (B, "ป.2", "เงิน"): (
        ("money_picture_p2", "fifty_satang_p2"),
        ("money_count_p2", "money_exchange_p2", "coins_make_amount_p2", "total_three_items_p2"),
        ("baht_satang_p2", "money_word_p2", "change_from_note_p2", "cheaper_by_p2"),
    ),
    (B, "ป.2", "เวลา"): (
        ("clock_read_p2", "time_notation_p2", "months_p2", "weeks_days_p2"),
        ("calendar_weekday", "hours_minutes_p2", "time_after_p2", "time_before_p2"),
        ("time_to_hour", "time_elapsed"),
    ),
    (B, "ป.2", "แผนภูมิรูปภาพ"): (
        ("pictograph_key_picture_p2", "pictograph", "pictograph_add_symbols_p2"),
        ("pictograph_compare_p2", "pictograph_total_p2", "pictograph_range_p2", "pictograph_order_p2"),
        ("pictograph_symbols_p2", "pictograph_true_statement_p2", "pictograph_two_rows_p2"),
    ),
    # ── ป.3 ──────────────────────────────────────────────────────────────
    (B, "ป.3", "ค่าประจำหลัก"): (
        ("number_reading_p3", "more_less_thousand_p3", "digit_place_p3"),
        ("place_value_expanded", "place_value_compose", "number_between_p3", "zeros_in_number_p3"),
        ("order_numbers_p3", "place_value_word_p3", "number_from_digits_p3"),
    ),
    (B, "ป.3", "การคูณ"): (
        ("times_table", "multiplication", "multiply_by_tens_p3"),
        ("area_model_p3", "one_digit_multiply", "multiply_2x1", "multiply_3x1_p3", "largest_product_p3"),
        ("multiply_4x1_p3", "multiplication_word_problem_p3"),
    ),
    (B, "ป.3", "การหาร"): (
        ("division_remainder", "divide_by_ten_p3", "half_of_p3"),
        ("division_long", "division_check_p3", "missing_divisor_p3", "divides_evenly_p3",
         "largest_quotient_p3"),
        ("division_word_problem_p3", "share_equally_p3"),
    ),
    (B, "ป.3", "เศษส่วน"): (
        ("fraction_picture_p3", "read_fraction", "unit_fraction_of_p3"),
        ("fraction_of_group_p3", "compare_fractions_p3", "like_fractions_addsub", "fraction_left_p3"),
        ("equivalent_fraction", "fraction_word_problem_p3", "fraction_who_more_p3"),
    ),
    (B, "ป.3", "แบบรูป"): (
        ("number_pattern_p3", "pattern_next_p3"),
        ("pattern_rule_p3", "growing_pattern_picture_p3", "pattern_far_term_p3",
         "pattern_two_missing_p3", "pattern_four_shapes_p3"),
        ("growing_pattern_p3", "pattern_spending_p3", "pattern_member_p3"),
    ),
    (B, "ป.3", "โจทย์ปัญหาระคน"): (
        ("mixed_ops_p3",),
        ("two_step_sentence_p3", "buy_two_kinds_p3", "two_rooms_compare_p3"),
        ("two_step_word_problem_p3", "buy_then_share_p3", "save_then_spend_p3", "empty_seats_p3",
         "loads_delivered_p3", "pages_left_p3"),
    ),
    (B, "ป.3", "การบวกและการลบ"): (
        ("add_sub_large_p3", "add_three_four_digit_p3"),
        ("missing_addsub_large_p3", "check_addsub_p3", "missing_digit_add_p3", "largest_result_p3"),
        ("addsub_word_large_p3", "how_many_more_p3", "money_left_two_buys_p3", "compare_two_sums_p3"),
    ),
    (B, "ป.3", "การวัด"): (
        ("measuring_tool_p3", "estimate_measure_p3", "convert_length_p3", "km_m_to_m_p3"),
        ("convert_weight_p3", "metric_ton_p3", "length_word_problem_p3", "cm_mm_to_mm_p3"),
        ("weight_word_problem_p3", "route_distance_p3"),
    ),
    (B, "ป.3", "ปริมาตรและความจุ"): (
        ("jug_picture_p3", "convert_volume_p3", "capacity_unit_p3", "l_ml_to_ml_p3"),
        ("kitchen_measures_p3", "bottles_total_ml_p3", "largest_capacity_p3"),
        ("capacity_word_problem_p3", "pours_to_fill_p3", "pour_left_p3"),
    ),
    (B, "ป.3", "รูปสมมาตร"): (
        ("symmetry_picture_p3", "symmetry_axes", "symmetric_shape_p3", "symmetry_fold_p3"),
        ("symmetry_letter", "symmetry_axis_direction_p3", "most_axes_p3"),
        ("symmetry_regular_polygon", "symmetry_word_p3", "symmetry_total_axes_p3"),
    ),
    (B, "ป.3", "เงิน"): (
        ("baht_satang_p3", "money_total", "buy_several_p3"),
        ("change_picture_p3", "income_expense_record_p3", "unit_price_p3", "baht_satang_add_p3"),
        ("make_change", "money_change_left", "daily_saving_p3"),
    ),
    (B, "ป.3", "เวลา"): (
        ("clock_24h_p3", "year_facts_p3", "hours_to_minutes_p3"),
        ("duration_p3", "clock_duration_p3", "minutes_to_hours_p3", "days_to_hours_p3",
         "calendar_date_weekday_p3"),
        ("time_word_problem_p3", "longest_activity_p3"),
    ),
    (B, "ป.3", "ตารางทางเดียว"): (
        ("table_most_p3", "table_range_p3"),
        ("table_read_p3", "pictograph_make_p3", "tally_to_table_p3", "table_order_p3",
         "table_count_above_p3"),
        ("table_sum", "table_two_rows_p3", "table_true_statement_p3"),
    ),
    # ── ป.4 ──────────────────────────────────────────────────────────────
    (B, "ป.4", "ค่าประจำหลัก"): (
        ("number_reading_p4", "more_less_large_p4", "digit_count_p4"),
        ("place_value_millions_p4", "expanded_to_number_p4", "number_between_p4", "zeros_in_number_p4"),
        ("compare_large_numbers_p4", "place_value_word_p4", "number_from_digits_p4"),
    ),
    (B, "ป.4", "การคูณยาว"): (
        ("multiply_by_tens", "multiply_by_hundreds_p4"),
        ("multiply_3x1", "multiply_partial_products_p4", "multiply_3x2_p4", "missing_factor_p4",
         "largest_product_p4"),
        ("multiply_2x2", "multiply_multistep_p4", "boxes_total_p4"),
    ),
    (B, "ป.4", "การหาร"): (
        ("division", "divide_by_hundreds_p4"),
        ("division_2digit", "missing_dividend_p4", "remainder_only_p4", "largest_quotient_p4",
         "divides_evenly_p4"),
        ("division_context_p4", "dividend_from_remainder_p4", "share_large_p4"),
    ),
    (B, "ป.4", "การประมาณค่า"): (
        ("rounding", "rounds_to_p4"),
        ("estimate_sum", "estimate_product", "largest_rounding_to_p4", "smallest_rounding_to_p4",
         "estimate_difference_p4", "estimate_quotient_p4"),
        ("estimate_word_problem_p4", "estimate_bill_p4"),
    ),
    (B, "ป.4", "การบวกและการลบ"): (
        ("add_sub_large_p4", "add_three_large_p4"),
        ("missing_addsub_large_p4", "check_addsub_p4", "missing_digit_add_p4", "largest_result_p4"),
        ("addsub_word_large_p4", "how_many_more_p4", "budget_left_p4", "compare_two_sums_p4"),
    ),
    (B, "ป.4", "โจทย์ปัญหาระคน"): (
        ("mixed_ops_p4",),
        ("two_step_sentence_p4", "story_for_sentence_p4", "round_trips_p4", "full_trays_p4"),
        ("two_step_word_problem_p4", "ticket_income_p4", "buy_two_kinds_p4", "cost_per_person_p4",
         "yearly_saving_p4"),
    ),
    (B, "ป.4", "เศษส่วน"): (
        ("fraction_bars_p4", "fraction_kinds_p4", "improper_mixed_p4", "equivalent_missing_p4"),
        ("compare_fractions_multiple_p4", "fraction_addsub_multiple_p4", "fraction_of_amount_p4",
         "make_one_whole_p4"),
        ("fraction_word_problem_p4", "amount_left_fraction_p4"),
    ),
    (B, "ป.4", "ทศนิยม"): (
        ("decimal_grid_p4", "decimal_reading_p4", "decimal_place_value", "decimal_as_fraction_p4"),
        ("decimal_compare_p4", "decimal_addsub_p4", "round_decimal_whole_p4", "decimal_between_p4"),
        ("decimal_word_problem_p4", "decimal_two_step_word_p4"),
    ),
    (B, "ป.4", "เวลา"): (
        ("time_units_p4", "decade_century_p4", "leap_year_p4"),
        ("calendar_word_problem_p4", "days_to_weeks_p4", "longest_duration_p4", "race_times_p4"),
        ("travel_time_p4", "stopwatch_difference_p4", "days_between_dates_p4"),
    ),
    (B, "ป.4", "เส้นตรงและมุม"): (
        ("classify_line", "line_ray_picture_p4", "classify_angle", "angle_kind_picture_p4", "name_angle_p4"),
        ("protractor_read_p4", "construct_angle_protractor_p4", "angle_complement_supplement"),
        ("angles_around_point_p4", "clock_angle_p4"),
    ),
    (B, "ป.4", "สี่เหลี่ยมมุมฉาก"): (
        ("rectangle_figure_p4", "rectangle_area_perimeter", "largest_area_p4", "largest_perimeter_p4"),
        ("rectangle_missing_side_p4", "construct_rectangle_p4", "area_when_doubled_p4",
         "l_shape_area_p4"),
        ("rectangle_word_problem_p4", "same_perimeter_area_p4"),
    ),
    (B, "ป.4", "การนำเสนอข้อมูล"): (
        ("two_way_table_read_p5", "two_way_grand_total_p4"),
        ("two_way_table_total_p5", "two_way_column_diff_p4", "two_way_row_most_p4",
         "two_way_cell_diff_p4", "two_way_two_rows_p4"),
        ("two_way_table_compare_p5", "two_way_true_statement_p4", "two_way_missing_cell_p4"),
    ),
    (B, "ป.4", "แผนภูมิแท่ง"): (
        ("bar_chart_picture_p4", "bar_chart_read_p4", "bar_total_p4"),
        ("bar_chart_diff", "bar_range_p4", "bar_order_p4", "bar_count_above_p4"),
        ("bar_chart_compare_p4", "bar_true_statement_p4", "bar_two_rows_p4"),
    ),
    # ── ป.5 ──────────────────────────────────────────────────────────────
    (B, "ป.5", "เศษส่วน"): (
        ("reduce_fraction", "improper_to_mixed", "order_fractions"),
        ("add_fractions", "sub_fractions", "add_mixed_numbers"),
        ("mul_fractions", "div_fractions", "mixed_fractions", "fraction_remaining_p5"),
    ),
    (B, "ป.5", "โจทย์ปัญหาเศษส่วน"): (
        ("fraction_of_amount_p5", "part_of_hour_p5"),
        ("fraction_word_addsub_p5", "whole_from_part_p5", "pieces_from_length_p5",
         "share_among_people_p5", "increase_by_fraction_p5"),
        ("fraction_word_muldiv_p5", "two_shares_compare_p5", "who_further_p5"),
    ),
    (B, "ป.5", "ทศนิยม"): (
        ("compare_decimals", "decimal_times_power_of_ten", "decimal_digit_value_p5"),
        ("fraction_to_decimal_p5", "decimal_multiply_p5", "round_decimal_p5", "decimal_order_p5"),
        ("decimal_divide_p5", "decimal_word_problem_p5", "estimate_decimal_product_p5"),
    ),
    (B, "ป.5", "บัญญัติไตรยางศ์"): (
        ("unit_price_p5", "exchange_money_p5"),
        ("rate_word_problem_p5", "fuel_for_trip_p5", "days_to_earn_p5", "how_many_for_money_p5",
         "printing_time_p5", "better_buy_p5"),
        ("recipe_scaling_p5", "workers_days_p5"),
    ),
    (B, "ป.5", "ร้อยละ"): (
        ("percent_grid_p5", "percent_of_number", "percent_to_decimal_p5"),
        ("find_percent_p5", "percent_of_quantity_p5", "percent_to_fraction_p5",
         "percent_increase_price_p5"),
        ("discount", "percent_two_step_p5", "percent_left_over_p5"),
    ),
    (B, "ป.5", "เส้นขนาน"): (
        ("parallel_pair_picture_p5", "parallel_concepts_p5", "parallel_daily_life_p5",
         "vertical_angle_p5"),
        ("parallel_angle_picture_p5", "corresponding_angle_p5", "alternate_from_sum_p5",
         "is_parallel_check_p5"),
        ("parallel_angles", "co_interior_from_difference_p5"),
    ),
    (B, "ป.5", "ชนิดของรูปสี่เหลี่ยม"): (
        ("quadrilateral_picture_p5", "classify_quadrilateral", "quadrilateral_diagonals_p5"),
        ("parallelogram_properties", "construct_quadrilateral_p5", "parallelogram_angle_p5",
         "trapezoid_angle_p5", "diagonal_length_p5"),
        ("quadrilateral_angle", "quadrilateral_missing_side_p5"),
    ),
    (B, "ป.5", "พื้นที่รูปสี่เหลี่ยม"): (
        ("parallelogram_area", "parallelogram_perimeter_p5", "rhombus_from_diagonals_p5"),
        ("quadrilateral_area_figure_p5", "trapezoid_area", "parallelogram_height_p5",
         "largest_quadrilateral_area_p5"),
        ("rhombus_kite_area_p5", "trapezoid_missing_side_p5", "tiling_cost_p5"),
    ),
    (B, "ป.5", "ปริมาตร"): (
        ("unit_cubes_p5", "rectangular_prism_volume", "cube_volume_p5", "litres_cubic_cm_p5"),
        ("cube_units_p5", "largest_box_volume_p5", "cubes_in_box_p5"),
        ("volume_capacity_p5", "water_rise_volume_p5", "fill_tank_time_p5"),
    ),
    (B, "ป.5", "การนำเสนอข้อมูล"): (
        ("line_graph_picture_p5", "line_graph_total_p5", "line_graph_highest_p5"),
        ("line_graph_change", "bar_chart_make_p5", "line_graph_count_rises_p5",
         "line_graph_count_above_p5", "line_graph_true_p5"),
        ("line_graph_problem_p5", "line_graph_next_p5"),
    ),
    (B, "ป.5", "ปริซึม"): (
        ("prism_parts_p5", "prism_or_not_p5", "prism_objects_p5", "prism_net_rectangles_p5"),
        ("prism_name_p5", "prism_base_from_faces_p5", "prism_faces_plus_corners_p5",
         "cube_from_wire_p5"),
        ("prism_counts_p5", "box_edges_total_p5"),
    ),
    (B, "ป.5", "ความยาวและน้ำหนัก"): (
        ("length_decimal_p5", "decimal_to_smaller_unit_p5", "suitable_unit_p5"),
        ("weight_decimal_p5", "add_across_units_p5", "heaviest_of_four_p5",
         "weight_difference_grams_p5", "add_mixed_units_p5"),
        ("measure_decimal_word_p5", "ribbon_left_p5"),
    ),
    # ── ป.6 ──────────────────────────────────────────────────────────────
    (B, "ป.6", "จำนวนเฉพาะ"): (
        ("factors_p6", "prime_or_composite", "next_prime_p6"),
        ("pick_prime", "prime_factorisation_p6", "largest_prime_factor_p6", "count_factors_p6"),
        ("smallest_prime_factor", "prime_word_p6", "sum_of_primes_p6"),
    ),
    (B, "ป.6", "ห.ร.ม. และ ค.ร.น."): (
        ("gcd", "lcm", "common_multiple_p6"),
        ("gcd_word_problem_p6", "lcm_word", "common_factors_count_p6", "buses_together_p6"),
        ("gcd_lcm_relation_p6", "gcd_lcm_three_p6", "tiles_to_square_p6"),
    ),
    (B, "ป.6", "ลำดับการดำเนินการ"): (
        ("order_of_ops_integers", "ooo_true_statement_p6"),
        ("order_of_ops_powers", "ooo_division_first_p6", "ooo_nested_p6", "ooo_decimal_p6",
         "ooo_missing_number_p6"),
        ("order_of_ops", "order_of_ops_word_p6", "change_after_shopping_p6"),
    ),
    (B, "ป.6", "ทศนิยม"): (
        ("fraction_to_decimal", "decimal_missing_factor_p6"),
        ("decimal_to_fraction", "divide_decimal_by_decimal_p6", "round_quotient_p6",
         "decimal_rectangle_area_p6"),
        ("decimal_ops", "decimal_word_problem_p6", "decimal_three_step_word_p6", "price_per_kilo_p6"),
    ),
    (B, "ป.6", "ร้อยละ"): (
        ("ratio_to_percent", "percent_to_ratio", "vat_p6"),
        ("profit_loss_p6", "simple_interest", "whole_from_percent_p6", "discount_percent_p6"),
        ("percent_change_p6", "cost_from_profit_p6", "compare_offers_p6"),
    ),
    (B, "ป.6", "อัตราส่วนและมาตราส่วน"): (
        ("write_ratio_p6", "equivalent_ratio_p6", "ratio_lowest_terms_p6"),
        ("map_scale", "ratio_word_problem_p6", "scale_to_km_p6", "scale_to_map_p6",
         "ratio_other_part_p6"),
        ("ratio_share_p6", "share_three_ways_p6"),
    ),
    (B, "ป.6", "แบบรูป"): (
        ("pattern_nth_term_p6", "pattern_next_term_p6", "repeating_colour_p6"),
        ("pattern_rule_expression_p6", "pattern_missing_middle_p6", "pattern_multiply_p6",
         "square_numbers_p6", "growing_difference_p6"),
        ("matchstick_pattern_p6", "pattern_which_term_p6"),
    ),
    (B, "ป.6", "ชนิดของรูปสามเหลี่ยม"): (
        ("triangle_type_picture_p6", "classify_by_sides_p6", "triangle_facts_p6",
         "right_triangle_other_angle_p6"),
        ("classify_triangle_by_angle", "construct_triangle_p6", "isosceles_base_angle_p6",
         "isosceles_top_angle_p6"),
        ("triangle_missing_angle", "isosceles_side_from_perimeter_p6"),
    ),
    (B, "ป.6", "พื้นที่รูปสามเหลี่ยม"): (
        ("triangle_area_figure_p6", "triangle_area", "right_triangle_area_p6"),
        ("triangle_missing_side_p6", "composite_area_p6", "largest_triangle_area_p6",
         "two_triangles_one_base_p6"),
        ("composite_area_figure_p6", "triangle_area_word_p6", "rectangle_minus_triangle_p6"),
    ),
    (B, "ป.6", "วงกลม"): (
        ("circle_parts", "radius_diameter_p6"),
        ("circle_area_circumference", "circumference_from_diameter_p6", "semicircle_area_p6",
         "wheel_turns_p6"),
        ("circle_radius_from_circumference", "circle_word_problem_p6", "semicircle_perimeter_p6",
         "ring_area_p6"),
    ),
    (B, "ป.6", "เศษส่วนและจำนวนคละ"): (
        ("order_mixed_numbers_p6", "mixed_to_improper_p6", "reciprocal_p6"),
        ("mixed_number_ops_p6", "mixed_times_whole_p6", "mixed_divide_whole_p6", "largest_fraction_p6",
         "fraction_missing_factor_p6"),
        ("fraction_multistep_word_p6", "part_of_part_p6"),
    ),
    (B, "ป.6", "รูปเรขาคณิต 3 มิติ"): (
        ("solid_counts_picture_p6", "solid_from_description_p6", "objects_as_solids_p6",
         "curved_surface_p6"),
        ("solid_faces_edges_vertices", "net_to_solid_p6", "pyramid_counts_p6", "cross_section_p6"),
        ("euler_formula", "euler_missing_count_p6"),
    ),
    (B, "ป.6", "ปริมาตรและพื้นที่ผิว"): (
        ("prism_volume", "cube_surface_area", "cube_edge_from_volume_p6"),
        ("composite_box_volume_p6", "box_surface_area_p6", "open_box_surface_p6",
         "cube_edge_from_surface_p6", "height_from_base_area_p6"),
        ("water_level_p6", "box_doubled_p6"),
    ),
    (B, "ป.6", "แผนภูมิรูปวงกลม"): (
        ("pie_chart_picture_p6", "pie_chart", "pie_largest_part_p6", "pie_missing_percent_p6"),
        ("pie_chart_amount_p6", "pie_angle_from_percent_p6", "pie_percent_from_angle_p6",
         "pie_two_parts_p6"),
        ("pie_chart_missing_p6", "pie_total_from_part_p6"),
    ),
    # ── ม.1 ──────────────────────────────────────────────────────────────
    (B, "ม.1", "จำนวนเต็ม"): (
        ("number_line_picture_m1", "integer_distance_m1",
         "integer_order_m1", "absolute_value_m1", "integer_properties_m1",
         "integer_largest_expression_m1", "number_line_moves_m1"),
        ("integer_addsub", "integer_muldiv",
         "integer_order_of_operations_m1",
         "integer_missing_number_m1", "integer_product_four_m1"),
        ("integer_four_ops", "integer_word_problem_m1",
         "integer_run_sum_m1"),
    ),
    (B, "ม.1", "เลขยกกำลัง"): (
        ("power_of_2", "power_of_negative", "zero_exponent",
         "powers_of_ten_m1", "compare_powers_m1", "write_as_power_m1"),
        ("product_rule", "power_rule", "scientific_to_decimal", "scientific_notation",
         "scientific_compare_m1",
         "quotient_rule_m1", "evaluate_powers_m1"),
        ("scientific_multiply", "scientific_notation_word_m1"),
    ),
    (B, "ม.1", "แยกตัวประกอบเฉพาะ"): (
        ("factor_tree_m1", "prime_factorization"),
        ("count_divisors",),
        ("largest_prime_factor", "prime_factor_word_m1"),
    ),
    (B, "ม.1", "จำนวนตรรกยะ"): (
        ("fraction_number_line_m1", "largest_rational",
         "rational_inverse_m1",
         "rational_absolute_m1", "mixed_number_m1"),
        ("signed_fraction_muldiv",
         "rational_between_m1", "fraction_power_m1",
         "nearest_integer_m1"),
        ("signed_fraction_ops", "signed_number_context_m1",
         "rational_mixed_ops_m1", "fraction_of_amount_m1",
         "portions_m1", "mixed_number_sum_m1"),
    ),
    (B, "ม.1", "ทศนิยมและเศษส่วน"): (
        ("terminating_or_repeating_m1",
         "fraction_to_decimal_m1", "compare_decimals_m1", "repeating_bar_m1",
         "decimal_place_value_m1"),
        ("signed_decimal_ops_m1",
         "decimal_to_fraction_m1", "round_decimal_m1", "order_fractions_decimals_m1",
         "decimal_multiply_m1", "decimal_divide_m1", "fraction_percent_m1"),
        ("repeating_decimal_to_fraction_m1",
         "decimal_money_m1",
         "decimal_measure_m1"),
    ),
    (B, "ม.1", "นิพจน์พีชคณิต"): (
        ("evaluate_expression",
         "like_terms_m1", "coefficient_m1",
         "like_terms_two_letters_m1"),
        ("evaluate_two_variables",
         "words_to_expression_m1", "formula_substitution_m1",
         "factor_out_number_m1", "evaluate_square_m1", "subtract_bracket_m1"),
        ("simplify_linear", "expression_word_m1",
         "pattern_rule_m1", "perimeter_expression_m1",
         "equal_expressions_m1"),
    ),
    (B, "ม.1", "สมการเชิงเส้น"): (
        ("balance_equation_m1", "linear_equation",
         "check_solution_m1"),
        ("linear_equation_both_sides", "linear_equation_brackets",
         "linear_equation_fractions_m1",
         "decimal_equation_m1"),
        ("linear_equation_setup_m1", "linear_word_problem_m1",
         "linear_fee_comparison_m1", "linear_remaining_fraction_m1", "linear_transfer_m1",
         "consecutive_numbers_m1", "age_problem_m1", "rectangle_equation_m1"),
    ),
    (B, "ม.1", "อัตราส่วนและสัดส่วน"): (
        ("simplify_ratio", "solve_proportion",
         "percent_of_m1", "equivalent_ratio_m1"),
        ("three_term_ratio_m1", "proportion_word_problem_m1",
         "ratio_difference_m1",
         "discount_m1", "speed_distance_time_m1"),
        ("percent_word_problem_m1", "inverse_work_proportion_m1", "map_area_scale_m1",
         "ratio_after_adding_m1",
         "better_buy_m1",
         "map_distance_m1"),
    ),
    (B, "ม.1", "กราฟความสัมพันธ์เชิงเส้น"): (
        ("linear_graph_read_m1", "linear_graph_point",
         "quadrant_m1", "point_on_line_m1",
         "rising_line_m1", "table_fits_rule_m1"),
        ("linear_relation_context_m1",
         "axis_intercepts_m1", "table_from_equation_m1", "grid_distance_m1",
         "cost_backwards_m1", "point_on_axis_m1"),
        ("table_to_linear_equation_m1",
         "rate_of_change_m1",
         "intercept_triangle_m1"),
    ),
    (B, "ม.1", "การสร้างทางเรขาคณิต"): (
        ("angle_bisector",
         "construction_tools_m1", "construction_first_step_m1",
         "construction_result_m1", "triangle_data_m1"),
        ("angle_bisector_measure",
         "construct_segment_length_m1", "segment_halving_m1", "triangle_from_sides_m1",
         "copied_angles_m1", "parallel_construction_m1"),
        ("perpendicular_bisector", "construct_angle_m1",
         "construct_angle_steps_m1",
         "bisectors_on_line_m1"),
    ),
    (B, "ม.1", "มิติสัมพันธ์ของรูปเรขาคณิต"): (
        ("cross_section_m1", "net_picture_m1",
         "solid_description_m1", "solid_parts_m1",
         "prism_rectangles_m1"),
        ("solid_nets_m1",
         "net_faces_m1", "wire_frame_m1",
         "die_faces_m1", "cylinder_net_m1"),
        ("cube_stack_m1",
         "euler_formula_m1", "painted_cube_m1",
         "cube_staircase_m1", "glued_cubes_m1"),
    ),
    (B, "ม.1", "สถิติ"): (
        ("double_bar_chart_m1", "frequency_table_m1", "mode_from_data",
         "statistical_question_m1", "data_display_m1", "pictograph_m1",
         "median_m1", "mode_from_table_m1", "data_collection_m1"),
        ("mean_from_data",
         "pie_chart_m1",
         "total_from_mean_m1"),
        ("mean_missing_value_m1",
         "monthly_values_m1",
         "mean_new_value_m1"),
    ),
    # ── ม.2 ──────────────────────────────────────────────────────────────
    (B, "ม.2", "จำนวนจริง"): (
        ("nth_root", "classify_real_number",
         "sqrt_of_square_m2", "real_number_facts_m2", "square_roots_both_m2"),
        ("roots_of_perfect_powers_m2", "pick_irrational", "sqrt_between_integers",
         "square_root_context_m2", "sqrt_estimate_m2",
         "cube_root_between_m2"),
        ("simplify_sqrt", "sqrt_product", "sqrt_measure_context_m2",
         "compare_surds_m2"),
    ),
    (B, "ม.2", "เลขยกกำลัง"): (
        ("power_of_product", "power_of_quotient", "negative_exponent",
         "negative_exponent_evaluate"),
        ("negative_exponent_simplify", "hard_product_with_negative",
         "hard_product_then_power", "hard_quotient_then_power", "hard_power_then_negative",
         "missing_exponent_m2",
         "exponent_equation_m2"),
        ("fractional_exponent", "fractional_exponent_evaluate", "radical_to_exponent",
         "exponent_compare_m2"),
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
        ("factor_common_m2", "factor_difference_squares_m2", "factor_identify_m2",
         "factor_perfect_square_check_m2", "factor_two_variable_m2"),
        ("factor_trinomial_m2", "factor_perfect_square_m2", "factor_missing_term_m2", "factor_grouping_m2",
         "factor_square_minus_square_m2", "factor_perfect_square_k_m2"),
        ("factor_apply_m2", "factor_leading_coeff_m2", "factor_number_trick_m2",
         "factor_four_terms_m2"),
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
        ("pythagoras", "pythagoras_figure_m2",
         "pythagoras_square_areas_m2"),
        ("pythagoras_triple_check", "pythagoras_diagonal", "pythagoras_isosceles_m2", "pythagoras_rectangle_m2",
         "pythagoras_rhombus_m2", "pythagoras_triangle_perimeter_m2"),
        ("pythagoras_grid_distance_m2", "pythagoras_word_problem_m2", "pythagoras_ladder_m2",
         "pythagoras_box_diagonal_m2",
         "pythagoras_trapezoid_m2", "pythagoras_two_step_m2"),
    ),
    (B, "ม.2", "การแปลงทางเรขาคณิต"): (
        ("reflect_point", "translate_point", "transformation_property_m2",
         "rotate_origin_m2", "name_the_move_m2"),
        ("coordinate_transform", "reflect_line_m2", "translation_vector_m2",
         "reflect_twice_m2", "reflection_distance_m2"),
        ("transformation_picture_m2", "rotation_about_center_m2", "translation_then_reflection_m2",
         "inverse_transformation_m2",
         "translate_then_turn_m2"),
    ),
    (B, "ม.2", "ความเท่ากันทุกประการ"): (
        ("congruence_case", "congruence_correspondence_m2", "congruence_proof_reason_m2",
         "congruence_name_case_m2"),
        ("congruent_sides", "congruence_picture_m2", "congruence_missing_condition_m2",
         "congruence_not_enough_m2",
         "congruence_perimeter_m2", "congruence_bisecting_diagonals_m2"),
        ("congruent_angles", "congruence_sides_algebra_m2", "congruence_angles_algebra_m2",
         "congruence_right_triangle_m2", "congruence_isosceles_median_m2"),
    ),
    (B, "ม.2", "เส้นขนาน"): (
        ("cointerior_angle", "parallel_reason_m2",
         "parallel_name_pair_m2"),
        ("transversal_picture_m2", "polygon_angle_sum", "parallel_algebra_m2", "parallel_test_m2",
         "parallel_named_angle_m2",
         "parallel_ratio_m2", "parallel_difference_m2"),
        ("transversal_angle_chain", "parallel_bend_m2", "parallel_triangle_m2",
         "parallel_bisectors_m2", "parallel_two_unknowns_m2"),
    ),
    (B, "ม.2", "การให้เหตุผลทางเรขาคณิต"): (
        ("construct_angle_m2", "isosceles_triangle_angle_m2", "polygon_exterior_m2",
         "largest_angle_side_m2"),
        ("exterior_angle_m2", "triangle_angle_algebra_m2", "vertical_angles_algebra_m2", "triangle_inequality_m2",
         "right_triangle_acute_m2", "triangle_exterior_sum_m2", "perpendicular_bisector_m2"),
        ("converse_statement_m2", "angle_bisector_triangle_m2", "isosceles_sides_m2",
         "complement_supplement_algebra_m2"),
    ),
    (B, "ม.2", "พื้นที่ผิวและปริมาตร"): (
        ("prism_surface_area_m2", "cylinder_volume", "prism_volume_base_m2", "scale_volume_m2",
         "prism_lateral_area_m2"),
        ("cylinder_surface_area_m2", "cylinder_dimension_m2", "volume_litres_m2",
         "cube_area_volume_m2"),
        ("prism_cylinder_volume_word_m2", "hollow_cylinder_m2", "box_with_hole_m2",
         "cups_to_fill_m2", "paint_room_m2", "melt_recast_m2"),
    ),
    (B, "ม.2", "สถิติ"): (
        ("dot_plot_picture_m2", "dot_plot_m2", "central_tendency", "mean_median_mode_m2",
         "median_even_m2", "class_interval_m2"),
        ("stem_and_leaf_m2", "histogram_picture_m2", "median_from_data",
         "mean_missing_value_m2", "frequency_percent_m2"),
        ("grouped_frequency_m2", "missing_frequency_mean_m2", "corrected_mean_m2", "mean_from_frequency_m2",
         "median_after_new_value_m2",
         "combined_mean_m2"),
    ),
    # ── ม.3 ──────────────────────────────────────────────────────────────
    (B, "ม.3", "อสมการเชิงเส้น"): (
        ("inequality", "inequality_largest_integer_m3"),
        ("inequality_negative_coefficient", "inequality_setup_m3", "inequality_fraction_m3",
         "inequality_both_sides_m3"),
        ("inequality_compound", "inequality_word_problem_m3", "inequality_order_properties_m3",
         "inequality_count_integers_m3"),
    ),
    (B, "ม.3", "กระจายทวินาม"): (
        ("expand_binomials", "difference_of_squares_ax_m3", "mental_product_m3"),
        ("expand_formula", "square_of_ax_plus_b_m3", "binomial_x_coefficient_m3",
         "expand_two_variables_m3", "mental_square_m3"),
        ("expand_three_terms", "product_minus_square_m3"),
    ),
    (B, "ม.3", "แยกตัวประกอบ"): (
        ("factor_special", "factor_perfect_square_m3"),
        ("factor_quadratic", "factor_cubic_common_m3", "factor_difference_of_squares_m3",
         "which_factor_m3", "factor_two_variables_m3"),
        ("factor_common_then_quadratic", "factor_cubic_grouping_m3", "factor_leading_two_m3"),
    ),
    (B, "ม.3", "กำลังสองสมบูรณ์"): (
        ("complete_square_constant", "vertex_from_completed_m3", "which_perfect_square_m3"),
        ("quadratic_vertex", "least_value_m3", "solve_by_square_root_m3", "greatest_value_m3"),
        ("vertex_form_convert", "vertex_context_m3", "completed_square_numbers_m3"),
    ),
    (B, "ม.3", "สมการกำลังสอง"): (
        ("quadratic_equation", "which_root_m3"),
        ("quadratic_formula_roots", "quadratic_sum_product_roots", "quadratic_discriminant_m3",
         "quadratic_root_count_m3", "quadratic_sum_of_roots_m3", "consecutive_product_m3"),
        ("quadratic_word_problem_m3", "rectangle_width_from_area_m3"),
    ),
    (B, "ม.3", "กราฟของฟังก์ชันกำลังสอง"): (
        ("parabola_graph_m3", "parabola_opens_m3", "parabola_y_intercept_m3"),
        ("parabola_vertex", "parabola_x_intercepts_m3", "parabola_extreme_value_m3",
         "point_on_parabola_m3", "parabola_shift_m3"),
        ("parabola_axis_intercept", "parabola_vertex_standard_m3"),
    ),
    (B, "ม.3", "ระบบสมการ"): (
        ("simultaneous_2var", "system_substitution", "system_sum_difference_m3", "system_which_pair_m3"),
        ("system_setup_m3", "system_x_plus_y_m3", "system_coins_m3", "system_ages_m3"),
        ("system_word_problem", "system_two_prices_m3"),
    ),
    (B, "ม.3", "ความคล้าย"): (
        ("similar_triangle_picture_m3", "similar_triangle", "similar_corresponding_angle_m3"),
        ("similar_shadow", "similar_figures_ratio_m3", "similar_scale_ratio_m3"),
        ("similar_ratio_area", "similar_parallel_segment_m3", "similar_remaining_area_m3",
         "similar_side_from_areas_m3"),
    ),
    (B, "ม.3", "อัตราส่วนตรีโกณมิติ"): (
        ("trig_special_values_m3", "trig_ratio_from_triple", "angle_from_ratio_m3",
         "special_angle_expression_m3"),
        ("special_triangle_picture_m3", "trig_application_height", "cos_from_sin_m3",
         "side_from_ratio_m3", "complementary_ratio_m3"),
        ("trig_word_problem_m3",),
    ),
    (B, "ม.3", "วงกลม"): (
        ("central_inscribed_angle", "inscribed_angle_semicircle", "inscribed_from_central_m3",
         "angles_same_arc_m3"),
        ("cyclic_quadrilateral", "circle_angle_picture_m3", "two_tangents_m3"),
        ("tangent_picture_m3", "tangent_length_m3", "chord_from_distance_m3"),
    ),
    (B, "ม.3", "พื้นที่ผิวและปริมาตร"): (
        ("pyramid_volume_m3", "cone_volume", "square_pyramid_volume_m3"),
        ("sphere_volume", "cone_sphere_surface_area_m3", "cylinder_volume_m3", "hemisphere_volume_m3"),
        ("solid_word_problem_m3", "cylinder_surface_m3", "cone_curved_from_height_m3"),
    ),
    (B, "ม.3", "สถิติ (แผนภาพกล่อง)"): (
        ("box_plot_picture_m2", "box_plot_range_m3", "box_plot_parts_m3"),
        ("box_plot_summary_m3", "boxplot_iqr", "box_plot_whisker_m3", "box_plot_middle_half_m3",
         "box_plot_two_medians_m3"),
        ("box_plot_compare_m2", "five_number_summary_m3"),
    ),
    (B, "ม.3", "ความน่าจะเป็นเบื้องต้น"): (
        ("probability_die_coin_m3", "probability_complement_m3"),
        ("spinner_probability_m3", "probability_bag_m3", "two_dice_sum_m3"),
        ("probability_two_events_m3", "probability_number_card_or_m3",
         "probability_two_colours_without_replacement_m3", "probability_add_balls_m3",
         "expected_count_m3"),
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
        ("compare_offers_m5", "interest_plan_m5", "compound_quarterly_m5",
         "regular_deposit_future_value_m5", "regular_payment_present_value_m5"),
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
        ("composite_formula", "composite_context_m4", "composite_equation_m4",
         "composite_sqrt_domain_m4", "composite_recover_inner_m4"),
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
        ("quadratic_range", "quadratic_range_half_line_m4", "quadratic_range_open_domain_m4",
         "quadratic_integer_optimum_m4"),
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
        ("sine_rule_angle_m5", "sine_rule_circumradius_m5", "sine_rule_area_from_angles_m5",
         "sine_rule_ambiguous_case_m5"),
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
        ("repeating_decimal_to_fraction", "infinite_series_word_m6", "telescoping_series_m6", "sigma_sums_m6",
         "alternating_geometric_sum_m6", "finite_telescoping_fraction_m6", "weighted_geometric_infinite_m6"),
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
        ("area_between_curves", "area_absolute_line_parabola_m6", "area_cubic_axis_lobes_m6",
         "area_crossing_curves_bounded_m6"),
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
