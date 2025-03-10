import React from 'react'
import { Link } from "react-router-dom";

export default function Topbar() {
  return (
    <div className="topbarContainer">
      <div className="topbarLeft">
        <span className="logo">
          <Link to="/public/" className="link-AdminSettings">
            CMSGRUPO2
          </Link>
        </span>
      </div>
      <div className="topbarRight">
        <span className="topbarLink">
          <Link to="/admin-login" className="link-AdminSettings">
            Admin-Login
          </Link>
        </span>
        <span className="topbarLink">
          <Link to="/admin/cms" className="link-AdminSettings">
            Admin-Settings
          </Link>
        </span>
      </div>
    </div>
  )
}
