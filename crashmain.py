# --- 5. The Target Gap Analyzer ---
        st.divider()
        st.subheader("🎯 Target Multiplier Gap Analysis")
        st.write("Analyze the 'droughts' between hitting a specific target.")
        
        target_multiplier = st.number_input("Enter target to analyze (e.g., 3.00):", min_value=1.01, value=3.00, step=0.10)
        
        if target_multiplier:
            gaps = []
            current_gap = 0
            hits = 0
            
            # Loop through our simulated history to count the gaps between hits
            for tick in market_history:
                if tick >= target_multiplier:
                    gaps.append(current_gap)
                    current_gap = 0
                    hits += 1
                else:
                    current_gap += 1
                    
            if hits > 0:
                avg_gap = sum(gaps) / len(gaps)
                max_gap = max(gaps)
                
                col_a, col_b, col_c = st.columns(3)
                col_a.metric(f"Total {target_multiplier}x Hits", f"{hits:,}")
                col_b.metric("Average Gap (Rounds)", f"{avg_gap:.1f}")
                col_c.metric("Longest Drought (Rounds)", f"{max_gap}")
                
                st.warning(f"💡 **Insight:** While a {target_multiplier}x hits every {avg_gap:.1f} rounds on average, the algorithm once went **{max_gap} rounds in a row** without hitting it.")
            else:
                st.write(f"A {target_multiplier}x never hit in this simulation.")
