<script lang="ts">
    import { Clock, ChefHat } from 'lucide-svelte'
    import { goto } from '$app/navigation'
    
    export let recipe: {
      id: number;
      name: string;
      description: string;
      image: string;
      duration: string;
      difficulty: string;
    }
  
    function viewRecipe() {
      goto(`/recipe/${recipe.id}`)
    }
  </script>
  
  <div class="recipe-card">
    <div class="image-container">
      <img src={recipe.image} alt={recipe.name} />
      <div class="overlay">
        <button class="view-btn" on:click={viewRecipe}>查看食譜</button>
      </div>
    </div>
    
    <div class="content">
      <h2>{recipe.name}</h2>
      <p>{recipe.description}</p>
      
      <div class="meta">
        <div class="meta-item">
          <Clock size={16} />
          <span>{recipe.duration}</span>
        </div>
        <div class="meta-item">
          <ChefHat size={16} />
          <span>{recipe.difficulty}</span>
        </div>
      </div>
    </div>
  </div>
  
  <style lang="scss">
    .recipe-card {
      background: rgba(255, 255, 255, 0.9);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 48px rgba(31, 38, 135, 0.15);
        
        .overlay {
          opacity: 1;
        }
      }
    }
  
    .image-container {
      position: relative;
      height: 240px;
      
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      
      .overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
      }
      
      .view-btn {
        padding: 0.8rem 1.5rem;
        background: white;
        color: #333;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transform: translateY(20px);
        transition: transform 0.3s ease;
        
        &:hover {
          background: #FF512F;
          color: white;
        }
      }
    }
  
    .content {
      padding: 1.5rem;
  
      h2 {
        margin: 0 0 0.8rem;
        font-size: 1.4rem;
        color: #333;
      }
  
      p {
        margin: 0 0 1rem;
        color: #666;
        line-height: 1.6;
      }
    }
  
    .meta {
      display: flex;
      gap: 1rem;
      
      .meta-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #666;
        font-size: 0.9rem;
      }
    }
  </style>