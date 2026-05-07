// Simple home page without JSX issues for now

export default function HomePage() {
  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(to bottom right, #dbeafe, #3b82f6)' }}>
      {/* Hero Section */}
      <div style={{ position: 'relative', overflow: 'hidden', backgroundColor: 'white', boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 32px' }}>
          <div style={{ position: 'relative', zIndex: 10, paddingBottom: '32px', paddingTop: '64px' }}>
            <div style={{ margin: '0 auto', maxWidth: '672px', textAlign: 'center' }}>
              <h1 style={{ fontSize: '48px', fontWeight: '800', letterSpacing: '-0.025em', color: '#111827', lineHeight: '1.2' }}>
                Find Your Perfect{' '}
                <span style={{ color: '#3b82f6' }}>Restaurant</span>
              </h1>
              <p style={{ margin: '24px auto 0', maxWidth: '672px', fontSize: '18px', lineHeight: '1.56', color: '#6b7280' }}>
                AI-powered restaurant recommendations tailored to your preferences. 
                Discover amazing dining experiences in your area.
              </p>
              
              {/* Quick Recommendation Form */}
              <div style={{ marginTop: '40px' }}>
                <div style={{ backgroundColor: 'white', padding: '32px', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', border: '1px solid #e5e7eb' }}>
                  <form style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '24px' }}>
                      <div>
                        <label htmlFor="location" style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                          Location
                        </label>
                        <input
                          type="text"
                          id="location"
                          name="location"
                          style={{ display: 'block', width: '100%', borderRadius: '6px', border: '1px solid #d1d5db', boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', fontSize: '14px' }}
                          placeholder="e.g., Bellandur, Indiranagar"
                        />
                      </div>
                      
                      <div>
                        <label htmlFor="budget" style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                          Budget Range
                        </label>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                          <input
                            type="number"
                            id="minBudget"
                            name="minBudget"
                            style={{ display: 'block', width: '100%', borderRadius: '6px', border: '1px solid #d1d5db', boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', fontSize: '14px' }}
                            placeholder="Min"
                          />
                          <input
                            type="number"
                            id="maxBudget"
                            name="maxBudget"
                            style={{ display: 'block', width: '100%', borderRadius: '6px', border: '1px solid #d1d5db', boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', fontSize: '14px' }}
                            placeholder="Max"
                          />
                        </div>
                      </div>
                      
                      <div>
                        <label htmlFor="rating" style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                          Minimum Rating
                        </label>
                        <select
                          id="rating"
                          name="rating"
                          style={{ display: 'block', width: '100%', borderRadius: '6px', border: '1px solid #d1d5db', boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', fontSize: '14px' }}
                        >
                          <option value="">Any Rating</option>
                          <option value="4.0">4.0+</option>
                          <option value="4.5">4.5+</option>
                          <option value="4.8">4.8+</option>
                        </select>
                      </div>
                      
                      <div>
                        <label htmlFor="cuisines" style={{ display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                          Preferred Cuisines
                        </label>
                        <input
                          type="text"
                          id="cuisines"
                          name="cuisines"
                          style={{ display: 'block', width: '100%', borderRadius: '6px', border: '1px solid #d1d5db', boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', fontSize: '14px' }}
                          placeholder="e.g., North Indian, Chinese, Italian"
                        />
                      </div>
                    </div>
                    
                    <div style={{ display: 'flex', justifyContent: 'center' }}>
                      <button
                        type="submit"
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          borderRadius: '6px',
                          border: 'none',
                          backgroundColor: '#3b82f6',
                          padding: '12px 24px',
                          fontSize: '16px',
                          fontWeight: '500',
                          color: 'white',
                          boxShadow: '0 1px 3px 0 rgba(59, 130, 246, 0.5)',
                          cursor: 'pointer'
                        }}
                      >
                        Get Recommendations
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div style={{ padding: '48px 0', backgroundColor: 'white' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 32px' }}>
          <div style={{ marginTop: '48px' }}>
            <div style={{ textAlign: 'center' }}>
              <h2 style={{ fontSize: '30px', fontWeight: '800', letterSpacing: '-0.025em', color: '#111827', lineHeight: '1.2' }}>
                Why Choose Our AI Recommendations?
              </h2>
              <p style={{ margin: '16px auto 0', maxWidth: '672px', fontSize: '20px', lineHeight: '1.5', color: '#6b7280' }}>
                Our intelligent system analyzes thousands of restaurants to find perfect match for your preferences.
              </p>
            </div>
            
            <div style={{ marginTop: '40px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '32px' }}>
                <div style={{ paddingTop: '24px' }}>
                  <div style={{ overflow: 'hidden', borderRadius: '8px', backgroundColor: '#f9fafb', padding: '32px', paddingBottom: '32px' }}>
                    <div style={{ marginTop: '-24px' }}>
                      <div>
                        <span style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          borderRadius: '6px',
                          backgroundColor: '#3b82f6',
                          padding: '12px',
                          boxShadow: '0 10px 15px -3px rgba(59, 130, 246, 0.5)'
                        }}>
                          🤖
                        </span>
                      </div>
                      <h3 style={{ marginTop: '32px', fontSize: '18px', fontWeight: '600', letterSpacing: '-0.025em', color: '#111827' }}>
                        AI-Powered
                      </h3>
                      <p style={{ marginTop: '20px', fontSize: '16px', lineHeight: '1.625', color: '#6b7280' }}>
                        Advanced machine learning algorithms analyze your preferences and provide personalized recommendations.
                      </p>
                    </div>
                  </div>
                </div>

                <div style={{ paddingTop: '24px' }}>
                  <div style={{ overflow: 'hidden', borderRadius: '8px', backgroundColor: '#f9fafb', padding: '32px', paddingBottom: '32px' }}>
                    <div style={{ marginTop: '-24px' }}>
                      <div>
                        <span style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          borderRadius: '6px',
                          backgroundColor: '#3b82f6',
                          padding: '12px',
                          boxShadow: '0 10px 15px -3px rgba(59, 130, 246, 0.5)'
                        }}>
                          ⚡
                        </span>
                      </div>
                      <h3 style={{ marginTop: '32px', fontSize: '18px', fontWeight: '600', letterSpacing: '-0.025em', color: '#111827' }}>
                        Real-time Data
                      </h3>
                      <p style={{ marginTop: '20px', fontSize: '16px', lineHeight: '1.625', color: '#6b7280' }}>
                        Up-to-date restaurant information including ratings, prices, and availability.
                      </p>
                    </div>
                  </div>
                </div>

                <div style={{ paddingTop: '24px' }}>
                  <div style={{ overflow: 'hidden', borderRadius: '8px', backgroundColor: '#f9fafb', padding: '32px', paddingBottom: '32px' }}>
                    <div style={{ marginTop: '-24px' }}>
                      <div>
                        <span style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          borderRadius: '6px',
                          backgroundColor: '#3b82f6',
                          padding: '12px',
                          boxShadow: '0 10px 15px -3px rgba(59, 130, 246, 0.5)'
                        }}>
                          🎯
                        </span>
                      </div>
                      <h3 style={{ marginTop: '32px', fontSize: '18px', fontWeight: '600', letterSpacing: '-0.025em', color: '#111827' }}>
                        Quality Assured
                      </h3>
                      <p style={{ marginTop: '20px', fontSize: '16px', lineHeight: '1.625', color: '#6b7280' }}>
                        Comprehensive filtering ensures you get restaurants that match your exact preferences.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div style={{ backgroundColor: '#3b82f6' }}>
        <div style={{ padding: '0 32px', paddingTop: '64px', paddingBottom: '64px' }}>
          <div style={{ textAlign: 'center' }}>
            <h2 style={{ fontSize: '30px', fontWeight: '800', letterSpacing: '-0.025em', color: 'white', lineHeight: '1.2' }}>
              Ready to Discover Amazing Restaurants?
            </h2>
            <p style={{ margin: '16px auto 0', maxWidth: '672px', fontSize: '20px', lineHeight: '1.5', color: '#dbeafe' }}>
              Get personalized recommendations in seconds. Start your culinary journey today.
            </p>
            <div style={{ marginTop: '32px', display: 'flex', justifyContent: 'center' }}>
              <div style={{ display: 'inline-flex', borderRadius: '6px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
                <a
                  href="/recommendations"
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor: 'white',
                    padding: '12px 24px',
                    fontSize: '16px',
                    fontWeight: '500',
                    color: '#3b82f6',
                    textDecoration: 'none',
                    cursor: 'pointer'
                  }}
                >
                  Get Started
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
