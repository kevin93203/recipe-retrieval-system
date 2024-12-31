<script lang="ts">
    import { Camera } from 'lucide-svelte'

    let { handleSearch, handleImageUpload} = $props();
    
    let searchInput = $state('')
    let fileInput: HTMLInputElement = $state()
  
    function handleSubmit() {
        console.log("handleSubmit")
        handleSearch(searchInput)
    }
  
    function handleFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        handleImageUpload(file)
      }
    }
  </script>
  
  <div class="search-container">
    <div class="search-box">
      <div class="search-input">
        <input
          type="text"
          bind:value={searchInput}
          placeholder="搜尋食譜或食材..."
          onkeyup={(e) => e.key === 'Enter' && handleSubmit()}
        />
        <button class="search-btn" onclick={handleSubmit}>搜尋</button>
      </div>
      
      <div class="divider">或</div>
      
      <div class="image-upload">
        <input
          type="file"
          bind:this={fileInput}
          accept="image/*"
          onchange={handleFileChange}
          style="display: none"
        />
        <button class="upload-btn" onclick={() => fileInput.click()}>
          <Camera size={20} />
          <span>上傳圖片搜尋</span>
        </button>
      </div>
    </div>
  </div>
  
  <style lang="scss">
    .search-container {
      max-width: 700px;
      margin: 0 auto;
      padding: 0 1rem;
    }
  
    .search-box {
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: 2rem;
      box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
    }
  
    .search-input {
      display: flex;
      gap: 0.5rem;
      
      input {
        flex: 1;
        padding: 1rem 1.5rem;
        border: 2px solid transparent;
        border-radius: 12px;
        font-size: 1rem;
        background: rgba(255, 255, 255, 0.9);
        transition: all 0.3s ease;
        
        &:focus {
          outline: none;
          border-color: #DD2476;
          box-shadow: 0 0 0 4px rgba(221, 36, 118, 0.1);
        }
      }
    }
  
    .search-btn {
      padding: 1rem 2rem;
      background: linear-gradient(45deg, #FF512F, #DD2476);
      color: white;
      border: none;
      border-radius: 12px;
      cursor: pointer;
      font-size: 1rem;
      font-weight: 600;
      transition: transform 0.2s;
      
      &:hover {
        transform: translateY(-2px);
      }
    }
  
    .divider {
      margin: 1.5rem 0;
      text-align: center;
      color: #666;
      position: relative;
      
      &::before,
      &::after {
        content: '';
        position: absolute;
        top: 50%;
        width: 45%;
        height: 1px;
        background: #ddd;
      }
      
      &::before {
        left: 0;
      }
      
      &::after {
        right: 0;
      }
    }
  
    .upload-btn {
      width: 100%;
      padding: 1rem;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      background: white;
      border: 2px dashed #ddd;
      border-radius: 12px;
      color: #666;
      cursor: pointer;
      transition: all 0.3s ease;
      
      &:hover {
        border-color: #DD2476;
        color: #DD2476;
        background: rgba(221, 36, 118, 0.05);
      }
    }
  </style>