#!/bin/bash

categories=("adhere" "violate")
subsets=("online_shopping" "social_discussion_forum")
countries=("India" "China" "U.S." "Indonesia" "Nigeria" "Brazil" "Russia" "Mexico" "Japan" "Ethiopia" "Egypt" "Iran" "France" "Thailand" "Argentina" "Morocco" "Saudi_Arabia")

# "non_agent", "non_agent_cs", "original", "examples_updated_2n1s", "examples_updated_2s", "system_prompt_updated", "system_prompt_updated_stop_2n", "system_prompt_updated_stop_2s"
prompt_method="original"
llm_model="gpt-4o"
api_key=""

echo "Starting S1 Generation..."

for country in "${countries[@]}"; do
  for category in "${categories[@]}"; do
    for subset in "${subsets[@]}"; do
      echo "\nRunning for Country: ${country}, Category: ${category}, Subset: ${subset}..."
      python ./llm_generation_s1.py \
        --country "${country}" \
        --category "${category}" \
        --subset "${subset}" \
        --prompt_method "${prompt_method}" \
        --llm_model "${llm_model}" \
        --api_key "${api_key}"
      
      if [ $? -eq 0 ]; then
        echo "✅ Successfully completed for Country: ${country}, Category: ${category}, Subset: ${subset}"
      else
        echo "❌ Error encountered for Country: ${country}, Category: ${category}, Subset: ${subset}"
      fi
    done
  done
done

echo "S1 Generation finished!"


echo "Starting S2 Generation..."

for country in "${countries[@]}"; do
    for subset in "${subsets[@]}"; do
        echo "\nRunning for Country: ${country}, Category: ${category}, Subset: ${subset}..."
        python ./llm_generation_s2.py \
        --country "${country}" \
        --subset "${subset}" \
        --prompt_method "${prompt_method}" \
        --llm_model "${llm_model}" \
        --api_key "${api_key}"
        
        if [ $? -eq 0 ]; then
        echo "✅ Successfully completed for Country: ${country}, Subset: ${subset}"
        else
        echo "❌ Error encountered for Country: ${country}, Subset: ${subset}"
        fi
    done
done

echo "S2 Generation finished!"


echo "Starting S1-A Helpfulness Evaluation..."

for country in "${countries[@]}"; do
    for subset in "${subsets[@]}"; do
        echo "\nRunning for Country: ${country}, Subset: ${subset}..."
        python ./llm_evaluation_s1a.py \
        --country "${country}" \
        --subset "${subset}" \
        --prompt_method "${prompt_method}" \
        --llm_model "${llm_model}" \
        --api_key "${api_key}"
        
        if [ $? -eq 0 ]; then
        echo "✅ Successfully completed for Country: ${country}, Subset: ${subset}"
        else
        echo "❌ Error encountered for Country: ${country}, Subset: ${subset}"
        fi
    done
done

echo "Starting S1-A Helpfulness Evaluation finished!"

echo "Starting S1-V Awareness Evaluation..."

for country in "${countries[@]}"; do
    for subset in "${subsets[@]}"; do
        echo "\nRunning for Country: ${country}, Subset: ${subset}..."
        python ./llm_evaluation_s1v_r1.py \
        --country "${country}" \
        --subset "${subset}" \
        --prompt_method "${prompt_method}" \
        --llm_model "${llm_model}" \
        --api_key "${api_key}"
        
        if [ $? -eq 0 ]; then
        echo "✅ Successfully completed for Country: ${country}, Subset: ${subset}"
        else
        echo "❌ Error encountered for Country: ${country}, Subset: ${subset}"
        fi
    done
done

echo "Starting S1-V Awareness Evaluation finished!"


echo "Starting S1-V Education Evaluation..."

for country in "${countries[@]}"; do
    for subset in "${subsets[@]}"; do
        echo "\nRunning for Country: ${country}, Subset: ${subset}..."
        python ./llm_evaluation_s1v_r2.py \
        --country "${country}" \
        --subset "${subset}" \
        --prompt_method "${prompt_method}" \
        --llm_model "${llm_model}" \
        --api_key "${api_key}"
        
        if [ $? -eq 0 ]; then
        echo "✅ Successfully completed for Country: ${country}, Subset: ${subset}"
        else
        echo "❌ Error encountered for Country: ${country}, Subset: ${subset}"
        fi
    done
done

echo "Starting S1-V Education Evaluation finished!"


echo "Starting S2 Violation Evaluation..."

for country in "${countries[@]}"; do
    echo "\nRunning for Country: ${country}, Subset: Social Discussion Forum..."
    python ./llm_evaluation_s2_social.py \
    --country "${country}" \
    --prompt_method "${prompt_method}" \
    --llm_model "${llm_model}" \
    --api_key "${api_key}"
    
    if [ $? -eq 0 ]; then
    echo "✅ Successfully completed for Country: ${country}, Subset: Social Discussion Forum"
    else
    echo "❌ Error encountered for Country: ${country}, Subset: Social Discussion Forum"
    fi
done

for country in "${countries[@]}"; do
    echo "\nRunning for Country: ${country}, Subset: Online Shopping..."
    python ./llm_evaluation_s2_shop_r1.py \
    --country "${country}" \
    --prompt_method "${prompt_method}" \
    --llm_model "${llm_model}" \
    --api_key "${api_key}"
    
    if [ $? -eq 0 ]; then
    echo "✅ Successfully completed for Country: ${country}, Subset: Online Shopping"
    else
    echo "❌ Error encountered for Country: ${country}, Subset: Online Shopping"
    fi
done

for country in "${countries[@]}"; do
    echo "\nRunning for Country: ${country}, Subset: Online Shopping..."
    python ./llm_evaluation_s2_shop_r2.py \
    --country "${country}" \
    --prompt_method "${prompt_method}" \
    --llm_model "${llm_model}" \
    --api_key "${api_key}"
    
    if [ $? -eq 0 ]; then
    echo "✅ Successfully completed for Country: ${country}, Subset: Online Shopping"
    else
    echo "❌ Error encountered for Country: ${country}, Subset: Online Shopping"
    fi
done

echo "Starting S2 Violation Evaluation finished!"